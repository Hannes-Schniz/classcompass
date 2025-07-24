FROM ubuntu:latest

RUN apt update
RUN apt upgrade -y

RUN apt install git -y

RUN apt install python3 -y

RUN apt install sqlite3 libsqlite3-dev -y

RUN useradd -ms /bin/bash navigator
USER navigator

WORKDIR /home/navigator

RUN git clone https://github.com/Hannes-Schniz/classcompass.git

RUN touch /var/spool/cron/crontabs/navigator

RUN echo "* * * * * bash /home/navigator/classcompass/exec.sh" >> /var/spool/cron/crontabs/navigator

RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r classcompass/requirements.txt


ENTRYPOINT [ "source /home/navigator/.venv/bin/activate; bash" ]

