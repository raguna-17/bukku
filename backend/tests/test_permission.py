# tests/test_permission.py
from app.models import User
from app.auth import create_access_token, get_password_hash

def create_user(db, email):
    user = User(email=email, hashed_password=get_password_hash("pw"))
    db.add(user)
    db.commit()
    return user

