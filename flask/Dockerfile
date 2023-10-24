FROM python:3.11-slim-buster
RUN apt update && \
    apt -y upgrade && \
    apt -y install build-essential libffi-dev

RUN pip install --upgrade -I pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN mkdir files
COPY --from=jerem0027/certificats:10-2023 /etc/certs /cert

COPY /app /app

WORKDIR /app

RUN mv server/envconfig_prod.py server/envconfig.py

CMD ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--certfile", "/cert/jeremiehenrion.pem-chain", "--keyfile", "/cert/jeremiehenrion.key", "app:app"]