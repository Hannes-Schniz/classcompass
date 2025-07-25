FROM ubuntu:latest

# ARG declarations for configuration variables from setupconfig.py
ARG CLASS_ID
ARG COLOR_PRIMARY
ARG COLOR_CANCELLED
ARG COLOR_CHANGED
ARG COLOR_EXAM
ARG WEEKS_AHEAD
ARG MAINTENANCE
ARG SHOWCANCELLED
ARG SHOWCHANGES

# ARG declarations for database setup variables from setupdb.py
ARG DB_PATH
ENV DB_PATH=${DB_PATH}
ARG SQL_DIR

# Virtual environment and source code paths
ENV VENV="/opt/venv/bin/activate"
ENV SOURCE="/home/navigator/classcompass"

RUN apt update
RUN apt upgrade -y

RUN apt install git -y

RUN apt install python3 -y

RUN apt install python3.12-venv -y

RUN apt install sqlite3 libsqlite3-dev -y

RUN apt install cron -y

RUN useradd -ms /bin/bash navigator

# Set up cron job to run the application handler every minute
RUN echo "* * * * * bash /home/navigator/classcompass/exec.sh" >> /var/spool/cron/crontabs/navigator

WORKDIR /home/navigator

# Clone the repository as the navigator user (non-root for security)
USER navigator
RUN git clone https://github.com/Hannes-Schniz/classcompass.git

USER root

# Create Python virtual environment in system location
# This isolates Python dependencies from the system Python installation
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate && pip install -r /home/navigator/classcompass/requirements.txt

RUN bash classcompass/setup.sh > /tmp/setup.log

# Configure the navigator user's shell to automatically activate the virtual environment
# This ensures Python dependencies are available when the user logs in
RUN echo "source /opt/venv/bin/activate" >> /home/navigator/.bashrc

CMD [ "/bin/bash" ]

