FROM docker.io/python:3.12.6-slim-bookworm AS python

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "EIS_test_task.wsgi:application"]