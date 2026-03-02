def create_user(client, email="auth@example.com", password="password123"):
    return client.post("/users/", json={
        "email": email,
        "password": password
    })


def test_login_success(client):
    create_user(client)

    res = client.post("/auth/login", json={
        "email": "auth@example.com",
        "password": "password123"
    })

    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    create_user(client)

    res = client.post("/auth/login", json={
        "email": "auth@example.com",
        "password": "wrong"
    })

    assert res.status_code == 400


def test_login_nonexistent_user(client):
    res = client.post("/auth/login", json={
        "email": "nouser@example.com",
        "password": "password123"
    })

    assert res.status_code == 400