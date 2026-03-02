def test_tag_reuse(client):
    headers = None

    # user作成
    client.post("/users/", json={
        "email": "tag@example.com",
        "password": "password123"
    })

    res = client.post("/auth/login", json={
        "email": "tag@example.com",
        "password": "password123"
    })

    headers = {"Authorization": f"Bearer {res.json()['access_token']}"}

    # 1回目
    client.post("/bookmarks/", json={
        "title": "A",
        "url": "https://a.com",
        "description": "",
        "tags": ["same"]
    }, headers=headers)

    # 2回目
    res = client.post("/bookmarks/", json={
        "title": "B",
        "url": "https://b.com",
        "description": "",
        "tags": ["same"]
    }, headers=headers)

    assert res.status_code == 200
    assert res.json()["tags"][0]["name"] == "same"