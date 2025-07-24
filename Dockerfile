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

RUN echo "* * * * * bash /home/navigator/classcompass/exec.sh"

