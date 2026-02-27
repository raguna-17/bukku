FROM python:3.11-slim

# 環境変数
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/backend

# 作業ディレクトリ
WORKDIR /backend

# 必要最小限のライブラリ
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY app /backend/app
COPY alembic.ini /backend/alembic.ini
COPY alembic /backend/alembic

EXPOSE 8000

# uvicorn 起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]