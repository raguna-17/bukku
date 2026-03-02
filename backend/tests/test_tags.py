API_PREFIX = "/api/v1"


def create_user_and_login(client, email="tag@example.com"):
    client.post(f"{API_PREFIX}/users/", json={
        "email": email,
        "password": "password123"
    })

    res = client.post(f"{API_PREFIX}/auth/login", json={
        "email": email,
        "password": "password123"
    })

    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_tag_reuse(client):
    headers = create_user_and_login(client)

    # 1回目
    client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "A",
        "url": "https://a.com",
        "description": "",
        "tags": ["same"]
    }, headers=headers)

    # 2回目
    res = client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "B",
        "url": "https://b.com",
        "description": "",
        "tags": ["same"]
    }, headers=headers)

    assert res.status_code == 200

    data = res.json()
    assert data["tags"][0]["name"] == "same"