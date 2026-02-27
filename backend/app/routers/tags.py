from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# ✅ 相対import（推奨）
from app.db import get_db
from app.models import Tag
from app.schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["Tags"])


# ======================
# Create Tag
# ======================
@router.post("/", response_model=TagRead)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    existing = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    try:
        db.commit()
        db.refresh(db_tag)
    except Exception:
        db.rollback()
        raise

    return db_tag


# ======================
# Get All Tags
# ======================
@router.get("/", response_model=list[TagRead])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


# ======================
# Delete Tag
# ======================
@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"detail": "Tag deleted"}