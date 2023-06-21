FROM python:3.9
WORKDIR /usr/src/app

COPY ./server.py /usr/src/app

RUN apt-get update
RUN apt-get install ncat -y

ENTRYPOINT ncat -lkp 9990 -e "/usr/bin/python3.9 /usr/src/app/server.py"
