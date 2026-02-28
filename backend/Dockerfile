# ビルド時にどのコンテキストか指定可能にする
ARG CONTEXT=backend
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# システム依存ライブラリ
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ARGを使ってCOPYパスを切り替え
# CONTEXT=backend -> Render用
# CONTEXT=.       -> CI用
COPY ${CONTEXT}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ${CONTEXT}/app ./app
COPY ${CONTEXT}/alembic.ini ./alembic.ini
COPY ${CONTEXT}/alembic ./alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "0"]