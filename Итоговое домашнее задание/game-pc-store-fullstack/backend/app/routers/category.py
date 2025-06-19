from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.utils.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(name: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.category.create_category(db=db, name=name)