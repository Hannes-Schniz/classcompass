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

RUN apt update
RUN apt upgrade -y

RUN apt install git -y

RUN apt install python3 -y

RUN apt install python3.12-venv -y

RUN apt install sqlite3 libsqlite3-dev -y

RUN apt install cron -y

RUN useradd -ms /bin/bash navigator

RUN echo "* * * * * bash /home/navigator/classcompass/exec.sh" >> /var/spool/cron/crontabs/navigator

WORKDIR /home/navigator

USER navigator
RUN git clone https://github.com/Hannes-Schniz/classcompass.git

USER root

RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate && pip install -r /home/navigator/classcompass/requirements.txt

ENV VENV="/opt/venv/bin/activate"
ENV SOURCE="/home/navigator/classcompass"

RUN bash classcompass/setup.sh > /tmp/setup.log

RUN echo "source /opt/venv/bin/activate" >> /home/navigator/.bashrc

CMD [ "/bin/bash" ]

