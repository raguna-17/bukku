# Bukku

JWT認証付きブックマーク管理API  
FastAPI + PostgreSQL + React(Vite)

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic
- JWT (python-jose)
- Argon2 (passlib)
- Docker

### Frontend
- React 19
- Vite

---

## Architecture

React → FastAPI (JWT認証) → PostgreSQL

- ユーザー単位データ分離
- Bookmark × Tag N:M構成
- UniqueConstraint(user_id, url)
- Connection Pool最適化
- CORS環境変数制御

---

## API

Base Path:

/api/v1

### Auth
POST /api/v1/auth/login

### Bookmarks（JWT必須）
GET /api/v1/bookmarks  
POST /api/v1/bookmarks  
PUT /api/v1/bookmarks/{id}  
DELETE /api/v1/bookmarks/{id}  

---

## Run (Docker)

### 1. backend/.env

```
POSTGRES_USER=xxx
POSTGRES_PASSWORD=xxx
POSTGRES_DB=xxx
DATABASE_URL=postgresql://xxx:xxx@db:5432/xxx

SECRET_KEY=xxx
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

FRONTEND_ORIGINS=http://localhost:5173
```

### 2. 起動

```
docker-compose up --build
```

Backend:
http://localhost:8000  
Docs:
http://localhost:8000/docs

---

## Migration

```
docker-compose exec backend alembic upgrade head
```

---

## Features

- JWT認証（Bearer）
- Argon2パスワードハッシュ
- N:Mタグ管理
- URL重複防止（ユーザー単位）
- Postgres Healthcheck
- SQLAlchemy Connection Pool

---

## Future Improvements

- Refresh Token
- Pagination
- Full-text Search
- CI/CD