# tests/test_auth.py
from app.auth import get_password_hash, verify_password, create_access_token

def test_password_hash_verify():
    pw = "secret123"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed)

def test_jwt_creation():
    token = create_access_token({"sub": "1"})
    assert isinstance(token, str)