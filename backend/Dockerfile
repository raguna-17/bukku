# ---------- Base Stage ----------
FROM python:3.11-slim AS base

WORKDIR /app

# Python依存関係インストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# アプリコピー
COPY app ./app

# ---------- Test Stage ----------
FROM base AS test

RUN pip install --no-cache-dir pytest pytest-cov httpx
COPY tests ./tests
COPY pytest.ini ./

# pytest 実行
RUN pytest

# ---------- Production Stage ----------
FROM python:3.11-slim AS prod

WORKDIR /app

# 本番用依存関係とアプリコピー
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /app /app

# 環境変数
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Render対応のポート
ENV PORT 8000

# uvicorn起動（RenderがPORTを指定する場合はそれを優先）
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]