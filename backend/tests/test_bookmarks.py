def create_user_and_login(client):
    client.post("/users/", json={
        "email": "bm@example.com",
        "password": "password123"
    })

    res = client.post("/auth/login", json={
        "email": "bm@example.com",
        "password": "password123"
    })

    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_bookmark(client):
    headers = create_user_and_login(client)

    res = client.post("/bookmarks/", json={
        "title": "Google",
        "url": "https://google.com",
        "description": "search",
        "tags": ["tech"]
    }, headers=headers)

    assert res.status_code == 200
    assert res.json()["title"] == "Google"
    assert len(res.json()["tags"]) == 1


def test_read_bookmarks(client):
    headers = create_user_and_login(client)

    client.post("/bookmarks/", json={
        "title": "Google",
        "url": "https://google.com",
        "description": "search",
        "tags": []
    }, headers=headers)

    res = client.get("/bookmarks/", headers=headers)

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_update_bookmark(client):
    headers = create_user_and_login(client)

    create_res = client.post("/bookmarks/", json={
        "title": "Old",
        "url": "https://example.com",
        "description": "old",
        "tags": []
    }, headers=headers)

    bookmark_id = create_res.json()["id"]

    res = client.put(f"/bookmarks/{bookmark_id}", json={
        "title": "New",
        "url": "https://example.com",
        "updated_at": "2024-01-01T00:00:00",
        "tags": ["updated"]
    }, headers=headers)

    assert res.status_code == 200
    assert res.json()["title"] == "New"
    assert len(res.json()["tags"]) == 1


def test_delete_bookmark(client):
    headers = create_user_and_login(client)

    create_res = client.post("/bookmarks/", json={
        "title": "Delete",
        "url": "https://delete.com",
        "description": "",
        "tags": []
    }, headers=headers)

    bookmark_id = create_res.json()["id"]

    res = client.delete(f"/bookmarks/{bookmark_id}", headers=headers)
    assert res.status_code == 200


def test_update_other_users_bookmark_404(client):
    # user1
    headers1 = create_user_and_login(client)

    create_res = client.post("/bookmarks/", json={
        "title": "Private",
        "url": "https://private.com",
        "description": "",
        "tags": []
    }, headers=headers1)

    bookmark_id = create_res.json()["id"]

    # user2
    client.post("/users/", json={
        "email": "other@example.com",
        "password": "password123"
    })

    res = client.post("/auth/login", json={
        "email": "other@example.com",
        "password": "password123"
    })

    headers2 = {"Authorization": f"Bearer {res.json()['access_token']}"}

    res = client.put(f"/bookmarks/{bookmark_id}", json={
        "title": "Hack",
        "url": "https://hack.com",
        "updated_at": "2024-01-01T00:00:00",
        "tags": []
    }, headers=headers2)

    assert res.status_code == 404