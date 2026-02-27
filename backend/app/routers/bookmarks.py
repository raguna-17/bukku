from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db import get_db
from ..models import Bookmark, Tag
from ..schemas import BookmarkCreate, BookmarkRead, BookmarkUpdate
from ..auth import get_current_user
from ..models import User
from app import db, models, schemas
from pydantic import HttpUrl

router = APIRouter(prefix="/bookmarks")

# Bookmark 作成
@router.put("/{bookmark_id}", response_model=BookmarkRead)
def update_bookmark(
    bookmark_id: int,
    bookmark: BookmarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_bookmark = (
        db.query(Bookmark)
        .filter(
            Bookmark.id == bookmark_id,
            Bookmark.user_id == current_user.id,
        )
        .first()
    )

    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    data = bookmark.model_dump(exclude_unset=True)

    # ===== Tags handling (safe & atomic) =====
    if "tags" in data:
        tag_objects = []
        for name in data["tags"]:
            tag = db.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.add(tag)
                try:
                    db.flush()  # DBに即反映（commit前）
                except IntegrityError:
                    db.rollback()
                    tag = db.query(Tag).filter_by(name=name).first()
            tag_objects.append(tag)

        db_bookmark.tags = tag_objects  # 完全置換（PUT semantics）

    # ===== Other fields =====
    for key, value in data.items():
        if key != "tags":
            # HttpUrlなら文字列に変換してからセット
            if isinstance(value, HttpUrl):
                value = str(value)
            setattr(db_bookmark, key, value)

    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

# Bookmark 削除
@router.delete("/{bookmark_id}")
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()

    if not db_bookmark:
        raise HTTPException(404, "Bookmark not found")

    db.delete(db_bookmark)
    db.commit()
    return {"detail": "Deleted"}


@router.post("/", response_model=BookmarkRead)
def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # タグ解決
    tag_objects = []
    for name in bookmark.tags:
        tag = db.query(Tag).filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
            try:
                db.flush()
            except IntegrityError:
                db.rollback()
                tag = db.query(Tag).filter_by(name=name).first()
        tag_objects.append(tag)

    # Bookmark 作成
    db_bookmark = Bookmark(
        title=bookmark.title,
        url=str(bookmark.url),  # HttpUrl -> str
        description=bookmark.description,
        user_id=current_user.id,
        tags=tag_objects
    )

    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


@router.get("/", response_model=list[BookmarkRead])
def read_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
    return bookmarks