FROM python:3.9.14-slim@sha256:f0687882d40d9813c46268585403aee057a7ffe7a4a7a27b5df243201a4b01fc
WORKDIR /app

RUN useradd tech

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh wait-for-it.sh

ENV FLASK_APP main.py

RUN chown -R tech:tech ./
USER tech

EXPOSE 5000
CMD [ "/bin/sh", "entrypoint.sh"]
