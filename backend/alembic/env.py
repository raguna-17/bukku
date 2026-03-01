# backend/alembic/env.py
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models import Base

# ログ設定
fileConfig(context.config.config_file_name)

# 本番/ローカルでは .env をロード、CI ではロードしない
if os.getenv("GITHUB_ACTIONS") != "true":
    from dotenv import load_dotenv
    load_dotenv()

# CLI 引数または環境変数で接続先を決定
db_url_arg = context.get_x_argument(as_dictionary=True).get("db_url")
DATABASE_URL = db_url_arg or  os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL は設定されていません")

target_metadata = Base.metadata

engine = engine_from_config(
    {"sqlalchemy.url": DATABASE_URL},
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()