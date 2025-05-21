from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from auth import (
    Token, User, authenticate_user,
    create_access_token, get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, timedelta
)
from database import Database

app = FastAPI()
db = Database()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_superuser: bool = False

@app.post("/auth/register", response_model=User)
async def register(user: UserCreate):
    existing_user = db.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return db.create_user(
        username=user.username,
        email=user.email,
        password=user.password,
        is_superuser=user.is_superuser
    )

@app.post("/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    # В реальном приложении здесь можно добавить логику инвалидации токена
    return {"message": "Successfully logged out"}

# Защищенные эндпоинты
@app.get("/students/", response_model=List[Student])
async def read_all_students(current_user: User = Depends(get_current_active_user)):
    return db.get_all_students()

@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate,
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create students"
        )
    return db.create_student(
        last_name=student.last_name,
        first_name=student.first_name,
        faculty=student.faculty,
        course=student.course,
        grade=student.grade
    )

# ... остальные CRUD эндпоинты с защитой ...