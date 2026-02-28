ARG CONTEXT=backend
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000   

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ${CONTEXT}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ${CONTEXT}/app ./app
COPY ${CONTEXT}/alembic.ini ./alembic.ini
COPY ${CONTEXT}/alembic ./alembic

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]