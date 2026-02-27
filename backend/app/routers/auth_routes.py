from fastapi import APIRouter, Body, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..auth import authenticate_user, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

# 入力モデルをここに書く（schemas を使わずにテスト）
class LoginForm(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=dict)
def login(form_data: LoginForm = Body(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}