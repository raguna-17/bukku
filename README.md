# Bukku

JWT認証付きブックマークAPI  
FastAPI + PostgreSQL + React (Vite)

---

## デモ

| サービス       | URL                                    |
|---------------|----------------------------------------|
| フロントエンド | https://bukku-furonto.onrender.com     |
| バックエンドAPI | https://bukku-bakku.onrender.com       |
| ドキュメント   | https://bukku-bakku.onrender.com/docs  |

---

## 技術スタック

### バックエンド
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic
- JWT (python-jose)
- Argon2 (passlib)
- Docker

### フロントエンド
- React 19
- Vite

---

## アーキテクチャ

React → FastAPI (JWT認証) → PostgreSQL


- ユーザー単位でデータを分離
- Bookmark × Tag の N:M 関係
- URL 重複防止（ユーザー単位）
- Connection Pool 最適化
- CORS は環境変数で制御

---

## API

ベースパス: `/api/v1`

| エンドポイント           | メソッド | 認証 | 説明              |
|--------------------------|--------|------|-----------------|
| /auth/login              | POST   | なし | ログイン           |
| /bookmarks               | GET    | 必須 | ブックマーク一覧取得 |
| /bookmarks               | POST   | 必須 | ブックマーク作成   |
| /bookmarks/{id}          | PUT    | 必須 | ブックマーク更新   |
| /bookmarks/{id}          | DELETE | 必須 | ブックマーク削除   |

---

## Dockerでの起動

### 1. backend/.env

```env
POSTGRES_USER=xxx
POSTGRES_PASSWORD=xxx
POSTGRES_DB=xxx
DATABASE_URL=postgresql://xxx:xxx@db:5432/xxx

SECRET_KEY=xxx
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

FRONTEND_ORIGINS=http://localhost:5173
```

### 2. 起動コマンド
docker-compose up --build

バックエンド: http://localhost:8000

ドキュメント: http://localhost:8000/docs


## マイグレーション
docker-compose exec backend alembic upgrade head


## 特徴

JWT認証（Bearer）

Argon2 パスワードハッシュ

N:M タグ管理

URL 重複防止（ユーザー単位）

PostgreSQL ヘルスチェック

SQLAlchemy Connection Pool