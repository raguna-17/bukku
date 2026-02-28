# backend/tests/conftest.py
import os
import time
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError

from app.db import Base, get_db
from app.main import app

# CI環境では必ず環境変数を使用
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL environment variable must be set in CI")

# エンジン作成
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DBが起動するまで待機して作成（最大30秒）
for _ in range(6):
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
        break
    except OperationalError:
        time.sleep(5)  # 5秒待機
else:
    raise RuntimeError("Database not reachable after waiting 30 seconds")

# DB fixture
@pytest.fixture(scope="function")
def db_session():
    # 各テスト関数前にテーブル作成
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        # drop_all はセッション終了時に1回だけ行う方が安定
        Base.metadata.drop_all(bind=engine)

# FastAPI dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    return TestClient(app)