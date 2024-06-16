FROM python:3.11-slim-buster
RUN apt update && \
    apt -y upgrade && \
    apt -y install build-essential libffi-dev

RUN pip install --upgrade -I pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN mkdir files

COPY /app /app
COPY CHANGELOG.md /app/static/CHANGELOG.md

WORKDIR /app

RUN mv server/envconfig_prod.py server/envconfig.py

CMD ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--certfile", "/certs/live/jeremiehenrion.eu/fullchain.pem", "--keyfile", "/certs/live/jeremiehenrion.eu/privkey.pem", "app:app"]