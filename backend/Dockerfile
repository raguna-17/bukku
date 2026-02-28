# Dockerfile
ARG CONTEXT=backend
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    MODE=production   

# 必要パッケージ（CI用に切り替え可能）
ARG CI=false
RUN apt-get update && apt-get install -y \
    $( [ "$CI" = "true" ] && echo "build-essential libpq-dev" ) \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY ${CONTEXT}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリとAlembicをコピー
COPY ${CONTEXT}/app ./app
COPY ${CONTEXT}/alembic.ini ./alembic.ini
COPY ${CONTEXT}/alembic ./alembic

# CMDをMODEで切り替え
CMD ["sh", "-c", "\
    if [ \"$MODE\" = 'test' ]; then \
    echo 'Test mode: waiting for DB and running migrations/tests'; \
    until pg_isready -h db -U testuser; do sleep 2; done; \
    alembic -x db_url=$TEST_DATABASE_URL upgrade head && pytest --maxfail=2; \
    else \
    echo 'Production mode: starting app'; \
    uvicorn app.main:app --host 0.0.0.0 --port $PORT; \
    fi"]