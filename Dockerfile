FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY dns_restful dns_restful
COPY deployments/production/main.py .

CMD [ "python3", "main.py"]