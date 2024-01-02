FROM python:latest

COPY Scripts app/

COPY Dataset app/Dataset

WORKDIR /app/Logs

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "script.py"]