# app/schemas.py
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import List, Optional
from fastapi import Form

# ======================
# Tag
# ======================

class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2 ORM対応


# ======================
# Bookmark
# ======================

class BookmarkBase(BaseModel):
    title: str
    url: HttpUrl
    description: Optional[str] = None


class BookmarkCreate(BookmarkBase):
    tags: List[str] = []   # タグ名で受け取る設計（実務的）


class BookmarkUpdate(BaseModel):
    title: str
    url: HttpUrl
    updated_at: datetime = datetime.utcnow()

    def dict_for_db(self):
        data = self.dict()
        data['url'] = str(data['url'])  # ←ここで文字列化
        return data


class BookmarkRead(BookmarkBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []

    class Config:
        from_attributes = True


# ======================
# User
# ======================

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    bookmarks: List[BookmarkRead] = []

    class Config:
        from_attributes = True

class LoginForm:
    def __init__(
        self,
        email: str = Form(...),  # username → email に変更
        password: str = Form(...),
        grant_type: str = Form("password")
    ):
        self.email = email
        self.password = password
        self.grant_type = grant_type