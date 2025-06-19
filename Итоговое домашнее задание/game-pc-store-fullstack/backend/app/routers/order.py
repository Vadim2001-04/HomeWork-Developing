from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.utils.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(user_id: int, db: Session = Depends(get_db)):
    order = crud.order.create_order_from_cart(db=db, user_id=user_id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return {"message": "Order created successfully"}