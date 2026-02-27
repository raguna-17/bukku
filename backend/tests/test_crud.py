# tests/test_crud.py
from app.models import User, Bookmark, Tag
from app.auth import get_password_hash
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# ----------------------------
# 既存テスト
# ----------------------------
def test_user_crud(db_session):
    user = User(email="a@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    db_session.commit()
    assert db_session.query(User).count() == 1

def test_bookmark_unique_constraint(db_session):
    user = User(email="b@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    db_session.commit()

    bm1 = Bookmark(title="t", url="http://x.com", user_id=user.id)
    bm2 = Bookmark(title="t", url="http://x.com", user_id=user.id)

    db_session.add(bm1)
    db_session.commit()

    db_session.add(bm2)
    with pytest.raises(Exception):
        db_session.commit()

# ----------------------------
# 追記：Bookmark CRUD
# ----------------------------
def test_bookmark_crud(db_session):
    # ユーザー作成
    user = User(email="crud@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    db_session.commit()

    # 1. Bookmark 作成
    bm = Bookmark(title="My Bookmark", url="http://example.com", description="desc", user_id=user.id)
    db_session.add(bm)
    db_session.commit()
    db_session.refresh(bm)
    assert bm.id is not None

    # 2. Bookmark 取得
    bm_from_db = db_session.query(Bookmark).filter_by(id=bm.id).first()
    assert bm_from_db.title == "My Bookmark"

    # 3. Bookmark 更新
    bm_from_db.title = "Updated"
    db_session.commit()
    updated = db_session.query(Bookmark).filter_by(id=bm.id).first()
    assert updated.title == "Updated"

    # 4. Bookmark 削除
    db_session.delete(updated)
    db_session.commit()
    assert db_session.query(Bookmark).filter_by(id=bm.id).first() is None

# ----------------------------
# 追記：Tag CRUD
# ----------------------------
def test_tag_crud(db_session):
    # タグ作成
    tag = Tag(name="python")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    assert tag.id is not None

    # 重複作成 → IntegrityError
    tag_dup = Tag(name="python")
    db_session.add(tag_dup)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # タグ取得
    fetched = db_session.query(Tag).filter_by(name="python").first()
    assert fetched is not None

    # タグ削除
    db_session.delete(fetched)
    db_session.commit()
    assert db_session.query(Tag).filter_by(name="python").first() is None