# ClassCompass

ClassCompass syncs class schedules from Untis into Google Calendar on a schedule and ships with a built‑in management web UI for configuration, credentials, and database inspection.

- Source of truth: Untis (via the Untis APIs)
- Destination: Google Calendar (via a service account)
- State: SQLite database (`maps.db`)
- Orchestration: cron inside the container calls the main job regularly
- Management: Flask web UI on port 5001

Looking for end‑user, step‑by‑step instructions for the web interface? See WEB_GUI.md.

## Features

- Automated sync job
  - Main runner `main/athena.py` fetches schedule data for a configurable look‑ahead window and pushes it to Google Calendar.
  - Robust cron execution using `exec.sh` with environment setup and logging.
- Web management GUI (`web/app.py`)
  - Dashboard with configuration and environment summaries + DB stats
  - Edit `config.json` (classID, color scheme, weeksAhead, maintenance, showCancelled, showChanges)
  - Edit `environment.json` (calendarID, cookie, anonymous-school, telegramToken, telegramChat)
  - Edit `credentials.json` (Google service account) with validation and a JSON preview
  - Database browser: list tables, paginate rows, run read‑only SELECT queries, view stats
  - Reset buttons for config and environment to defaults
- SQLite data model (created by `setup/setupdb.py`)
  - `classes(batchID, date, startTime, endTime, type, state, stateDetail, room, subject, substituteText)`
  - `diff(...)` holds before/after changes for schedule differences
- Dockerized runtime
  - Ubuntu base with a non‑root `navigator` user
  - Python venv in `/opt/venv` and dependencies from `setup/requirements.txt`
  - Cron installed and enabled; job runs every 5 minutes by default
  - Web UI started in background; logs written to `/var/log/webserver.log` and `/var/log/classcompass-cron.log`
- CI/CD with multi‑arch Docker images (x86_64, ARMv7, ARM64)
  - GitHub Actions workflows publish images for stable and experimental branches
  - QEMU + Buildx enable building ARM images for Raspberry Pi

## Repository layout

- `main/` — core logic
  - `_schedule/untis_connector.py`, `_schedule/untisDataHandler.py` — fetch Untis data
  - `_calendar/google_cal_connector.py`, `_calendar/calendarDataHandler.py` — write to Google Calendar
  - `_database/sqliteConnector.py` — DB interactions
  - `configReader.py` — parse `config.json`
  - `athena.py` — orchestrates a full sync run
- `web/` — Flask management GUI
  - `app.py` — routes for dashboard, config, environment, credentials, database APIs
  - `templates/*.html` — pages for dashboard, config, environment, database, credentials
- `setup/` — initialization helpers
  - `requirements.txt` — Python deps
  - `setupdb.py` — creates the SQLite schema
  - `setupconfig.py` — generates default `config.json`, `environment.json`, `credentials.json`
  - `sql/` — SQL schema files
  - `Dockerfile_local`, `Dockerfile_stable`, `Dockerfile_experimental` — container images
- Root scripts
  - `exec.sh` — cron entrypoint that activates the venv and runs `main/athena.py`
  - `setup.sh` — runs DB and config initialization
- `tooling/` — optional helpers (calendar sharing, admin CLI, etc.)

## Configuration files

- `config.json` — runtime options consumed by `athena.py`
  - `classID` (string)
  - `color-scheme.primary|cancelled|changed|exam` (strings/IDs)
  - `weeksAhead` (int)
  - `maintenance`, `showCancelled`, `showChanges` (bool)
- `environment.json` — integration values
  - `calendarID`, `cookie`, `anonymous-school`, `telegramToken`, `telegramChat`
- `credentials.json` — Google service account credentials with Calendar API access
  - Must be a valid service account JSON that has permission to the target calendar

All three files can be created/updated via the web UI and are generated with sane defaults by `setup/setupconfig.py`.

## Quick start (Docker)

The repository provides three Dockerfiles:

- `setup/Dockerfile_local` — build from your working tree
- `setup/Dockerfile_stable` — clone the `deploy_stable` branch inside the image
- `setup/Dockerfile_experimental` — clone the `deploy_experimental` branch inside the image

Build and run locally:

```bash
# From the repo root
docker build -f setup/Dockerfile_local -t classcompass:local .

# Run the container (exposes the web UI on 5001)
docker run --name classcompass \
  -p 5001:5001 \
  classcompass:local
```

Or use a published image from Docker Hub (stable):

```bash
docker pull hannesschniz/classcompass:stable

docker run --name classcompass \
  -p 5001:5001 \
  hannesschniz/classcompass:stable
```

Then open http://localhost:5001 and:

- Configure `config.json`
- Enter your `environment.json` values
- Paste your Google service account `credentials.json`

The cron job inside the container executes every 5 minutes and logs to `/var/log/classcompass-cron.log`.

Notes

- By default, the SQLite DB is at `/home/navigator/classcompass/maps.db` (inside the container). To persist it on the host, mount a volume to that path.
- The web UI runs as part of the same container and is started by `/start.sh`.

### Raspberry Pi / ARM

Multi‑arch images are published by CI. Use the ARM tags on Pi:

```bash
docker pull hannesschniz/classcompass:arm-stable         # stable ARM (arm/v7 + arm64)
docker pull hannesschniz/classcompass:arm-experimental   # experimental ARM
```

Or rely on Docker’s platform matching with a multi‑arch manifest (when available). The workflows set up QEMU + Buildx to produce ARM layers.

## Local development (no Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r setup/requirements.txt

# Initialize config and database
python3 setup/setupdb.py
python3 setup/setupconfig.py

# Start the web UI
python3 web/app.py  # serves on http://localhost:5001

# Run a sync pass manually
bash ./exec.sh
```

If you want to run it on a schedule locally, add a crontab entry (example: every 5 minutes):

```bash
*/5 * * * * cd /path/to/classcompass && bash ./exec.sh >> /var/log/classcompass-cron.log 2>&1
```

## Runtime details

- Cron setup in images
  - A `navigator` user is created.
  - Crontab: runs `bash /home/navigator/classcompass/exec.sh` at 0,5,10,…,55 minutes.
  - Logs: `/var/log/classcompass-cron.log` (job), `/var/log/webserver.log` (Flask), `/var/log/syslog` (cron daemon).
- `exec.sh`
  - Exports `VENV`, `SOURCE`, `DB_PATH` defaults
  - Activates `/opt/venv`
  - `cd` into the source directory and runs `python3 main/athena.py`
- Database
  - Created by `setup/setupdb.py` from SQL in `setup/sql/`
  - Default path: `maps.db` (inside repo root or as overridden by `DB_PATH`)
- Web UI endpoints (high level)
  - `/` dashboard, `/config`, `/environment`, `/database`, `/edit-credentials`
  - JSON APIs under `/api/*` and reset endpoints under `/reset/*`

## Configuration via environment variables

`setup/setupconfig.py` reads the following to generate `config.json` (defaults in parentheses):

- `CLASS_ID` (0)
- `COLOR_PRIMARY` (1)
- `COLOR_CANCELLED` (11)
- `COLOR_CHANGED` (5)
- `COLOR_EXAM` (10)
- `WEEKS_AHEAD` (3)
- `MAINTENANCE` (false)
- `SHOW_CANCELLED` (false)
- `SHOW_CHANGES` (false)

Database setup:

- `DB_PATH` — SQLite file path (default `maps.db`)
- `SQL_DIR` — path to SQL schema files (default `setup/sql`)

These are primarily used during image build and setup.

## CI/CD

GitHub Actions workflows publish images on branch pushes:

- `deploy_stable` → Dockerfiles `*_stable` and tags: `latest`, `v1.0.0`, `stable` + ARM variants (`arm-stable`, etc.)
- `deploy_experimental` → tags: `experimental` + ARM variants (`arm-experimental`)

Secrets expected in the repo:

- `DOCKERHUB_UNAME` — Docker Hub username
- `DOCKERHUB` — Docker Hub access token/password

Buildx and QEMU are used to build multi‑architecture images for ARM devices.

## Security notes

- `credentials.json` contains sensitive keys. Do not commit real credentials to version control. Prefer mounting the file at runtime or managing it via the web UI in a controlled environment.
- The management web UI does not enforce authentication by default. Only expose it to trusted networks or add reverse‑proxy auth.
- Limit container privileges and use volumes to persist only what’s necessary (e.g., the database file).

## Troubleshooting

- “exec format error” on Raspberry Pi: make sure you pull the ARM image tags (`arm-stable` / `arm-experimental`) or build with Buildx targeting `linux/arm/v7` or `linux/arm64`.
- Cron isn’t running: check `/var/log/syslog` for cron daemon logs and `/var/log/classcompass-cron.log` for job output. Ensure the crontab is loaded for user `navigator`.
- `athena.py` path errors: verify `SOURCE` points to the repo directory; `exec.sh` prints diagnostics for current directory and variables.

## License

TBD

## Contributing

Issues and PRs are welcome. Please avoid including sensitive credentials in commits.
