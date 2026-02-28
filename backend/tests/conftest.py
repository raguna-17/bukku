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

# CI/テスト用 DB URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL 環境変数が設定されていません")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB作成を安全に待機
for _ in range(6):
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
        break
    except OperationalError:
        time.sleep(5)
else:
    raise RuntimeError("Database に接続できません。DBが起動しているか確認してください")

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
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