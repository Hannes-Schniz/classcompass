# ClassCompass Web GUI and End‑User Setup

This guide walks you through using the built‑in web interface to configure ClassCompass and get your class schedule syncing to Google Calendar.

The web UI runs on port 5001 by default. Once the container or app is running, open:

- http://localhost:5001 (same machine)
- http://<server-ip>:5001 (remote server)

If you’re not using Docker, see Local development in the main README.

## First‑run checklist

1. Prepare your Google service account credentials

- In Google Cloud Console, create a project and enable the Google Calendar API.
- Create a Service Account and generate a JSON key (download `credentials.json`).
- Copy the service account email (ends with `iam.gserviceaccount.com`). You’ll share your calendar with this email later.

2. Identify your target Google Calendar

- Open Google Calendar (web) → Settings for the calendar you want to sync into.
- Copy the Calendar ID (looks like an email address).
- Share the calendar with your Service Account email with permission to Make changes to events.

3. WebUntis access (school system)

- You’ll need:
  - The “anonymous school” identifier (as used by your Untis instance)
  - A valid session cookie (if your setup requires it)

4. Optional: Telegram notifications

- Create a bot with @BotFather and note the bot token.
- Find your chat ID (a direct chat or group) to receive notifications.

## Using the web interface

### 1. Credentials page (Edit Credentials)

- Navigate to the “Credentials” page from the top navigation.
- Paste the content of your Google Cloud `credentials.json` exactly as downloaded. Ensure the `private_key` keeps its line breaks.
- Click Save. A backup of any prior credentials is kept with a timestamped `.bak.*` suffix.

Security tip: Only paste credentials over a secure connection and never commit `credentials.json` to version control.

### 2. Environment page

Manage external service settings.

- Google Calendar
  - Calendar ID: paste the ID you copied from Calendar settings.
- School system (WebUntis)
  - Anonymous School: your school identifier
  - Session Cookie: a valid cookie string if required for access
- Telegram (optional)
  - Bot Token: from @BotFather
  - Chat ID: destination chat

Use the Preview JSON button to quickly review your current values (it masks sensitive parts). The Test Connections button runs basic presence checks for required fields.

Click Save Environment to write changes to `environment.json`.

### 3. Configuration page

General runtime options stored in `config.json`.

- Class ID: your Untis class identifier
- Color scheme (primary, cancelled, changed, exam): Google Calendar color IDs
- Weeks Ahead: how far into the future to fetch
- Maintenance, Show Cancelled, Show Changes: runtime toggles

You can reset configuration to defaults with the Reset button.

### 4. Dashboard

Shows a quick overview:

- Current configuration and environment snippets
- Database statistics: classes count, batches, latest batch info, diff entries, and date range

### 5. Database browser

Powerful read‑only view of your SQLite data.

- Tables list: pick a table to view
- Paginated results with column headers
- Run custom queries: Only SELECT statements are allowed for safety
- Stats endpoint summarizes rows and ranges

Use this to troubleshoot what was fetched from Untis and what will be sent to Google Calendar.

## Triggering a sync

ClassCompass runs on a schedule via cron in the Docker images (every 5 minutes). For an immediate run:

- In Docker: execute the job inside the container
  - Example: `docker exec -it <container_name> bash -lc "/home/navigator/classcompass/exec.sh"`
- Without Docker: run from your virtual environment
  - `bash ./exec.sh`

Monitor logs:

- Web server: `/var/log/webserver.log`
- Cron job: `/var/log/classcompass-cron.log`
- Cron daemon (inside container): `/var/log/syslog`

## Common pitfalls and tips

- Calendar sharing: If events don’t appear, ensure the target calendar is shared with your Service Account email with write permissions.
- Credentials format: Keep the `private_key` field exactly as provided (multiline with `-----BEGIN PRIVATE KEY-----` … `-----END PRIVATE KEY-----`).
- Environment values: Make sure `calendarID` is set and WebUntis details are correct.
- Timezone: The application uses Europe/Berlin in the Google connector. Adjust in code if your deployment needs another timezone.
- Database location: By default the DB is `maps.db`. In Docker it lives at `/home/navigator/classcompass/maps.db`. Use a volume to persist it.
- Security: The web UI has no built‑in auth. Restrict network access or put it behind a reverse proxy with authentication.

## Where the files live

- `credentials.json` — Google service account credentials
- `environment.json` — calendar ID, school cookie/ID, Telegram token/chat
- `config.json` — classID, color scheme, weeksAhead, feature toggles
- `maps.db` — SQLite database storing fetched classes and diffs

All are editable via the web interface.

## Need help?

Check the Troubleshooting section in the main README and the logs listed above. If you still get stuck, open an issue and include non‑sensitive logs and details about your environment.
