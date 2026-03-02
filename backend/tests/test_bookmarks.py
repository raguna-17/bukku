API_PREFIX = "/api/v1"


def create_user_and_login(client, email="bm@example.com"):
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


def test_create_bookmark(client):
    headers = create_user_and_login(client)

    res = client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "Google",
        "url": "https://google.com",
        "description": "search",
        "tags": ["tech"]
    }, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Google"
    assert len(data["tags"]) == 1


def test_read_bookmarks(client):
    headers = create_user_and_login(client)

    client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "Google",
        "url": "https://google.com",
        "description": "search",
        "tags": []
    }, headers=headers)

    res = client.get(f"{API_PREFIX}/bookmarks/", headers=headers)

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_update_bookmark(client):
    headers = create_user_and_login(client)

    create_res = client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "Old",
        "url": "https://example.com",
        "description": "old",
        "tags": []
    }, headers=headers)

    bookmark_id = create_res.json()["id"]

    res = client.put(f"{API_PREFIX}/bookmarks/{bookmark_id}", json={
        "title": "New",
        "url": "https://example.com",
        "description": "updated",
        "tags": ["updated"]
    }, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "New"
    assert len(data["tags"]) == 1


def test_delete_bookmark(client):
    headers = create_user_and_login(client)

    create_res = client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "Delete",
        "url": "https://delete.com",
        "description": "",
        "tags": []
    }, headers=headers)

    bookmark_id = create_res.json()["id"]

    res = client.delete(f"{API_PREFIX}/bookmarks/{bookmark_id}", headers=headers)

    assert res.status_code == 200


def test_update_other_users_bookmark_404(client):
    # user1
    headers1 = create_user_and_login(client, email="user1@example.com")

    create_res = client.post(f"{API_PREFIX}/bookmarks/", json={
        "title": "Private",
        "url": "https://private.com",
        "description": "",
        "tags": []
    }, headers=headers1)

    bookmark_id = create_res.json()["id"]

    # user2
    headers2 = create_user_and_login(client, email="user2@example.com")

    res = client.put(f"{API_PREFIX}/bookmarks/{bookmark_id}", json={
        "title": "Hack",
        "url": "https://hack.com",
        "description": "hacked",
        "tags": []
    }, headers=headers2)

    assert res.status_code == 404