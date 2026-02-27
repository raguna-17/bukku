# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db
from app.models import User
from app.auth import get_password_hash, create_access_token

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def test_user(db_session):
    user = User(email="api@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture()
def token(test_user):
    return create_access_token({"sub": str(test_user.id)})

@pytest.fixture()
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ----------------------------
# Bookmark API Tests
# ----------------------------
def test_bookmark_crud(client, auth_headers):
    # Create
    res = client.post("/api/v1/bookmarks/", json={
        "title":"API BM",
        "url":"http://example.com",
        "description":"desc",
        "tags":["python"]
    }, headers=auth_headers)
    assert res.status_code == 200
    bm_id = res.json()["id"]

    # Read
    res = client.get("/api/v1/bookmarks/", headers=auth_headers)
    assert res.status_code == 200
    assert any(b["id"] == bm_id for b in res.json())

    # Update
    res = client.put(f"/api/v1/bookmarks/{bm_id}", json={
        "title":"Updated",
        "url":"http://example.com",
        "updated_at":"2026-02-26T00:00:00Z"
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Updated"

    # Delete
    res = client.delete(f"/api/v1/bookmarks/{bm_id}", headers=auth_headers)
    assert res.status_code == 200

# ----------------------------
# Tag API Tests
# ----------------------------
def test_tag_crud(client, auth_headers):
    # Create
    res = client.post("/api/v1/tags/", json={"name":"pytest"}, headers=auth_headers)
    assert res.status_code == 200
    tag_id = res.json()["id"]

    # Duplicate → 400
    res = client.post("/api/v1/tags/", json={"name":"pytest"}, headers=auth_headers)
    assert res.status_code == 400

    # List
    res = client.get("/api/v1/tags/", headers=auth_headers)
    assert res.status_code == 200
    assert any(t["id"] == tag_id for t in res.json())

    # Delete
    res = client.delete(f"/api/v1/tags/{tag_id}", headers=auth_headers)
    assert res.status_code == 200

# ----------------------------
# OpenAPI Test
# ----------------------------
def test_openapi(client):
    res = client.get("/openapi.json")
    assert res.status_code == 200