FROM arm32v7/python:3.11-slim-buster
RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

COPY apis/flask/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN mkdir files
COPY apis/flask/cert /cert

COPY apis/flask/app /app

WORKDIR /app

RUN mv server/envconfig_prod.py server/envconfig.py

CMD ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--certfile", "/cert/jeremiehenrion.pem", "--keyfile", "/cert/jeremiehenrion.key", "app:app"]