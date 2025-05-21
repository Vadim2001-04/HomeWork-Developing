from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.utils.hashing import verify_password
from app.utils.database import get_db
from app.core.config import settings
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}