FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY celery_app.py .

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
