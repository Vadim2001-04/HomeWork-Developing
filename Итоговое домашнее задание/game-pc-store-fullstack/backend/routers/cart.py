from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas import CartItemCreate
from app.utils.database import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    return crud.cart.add_to_cart(db=db, user_id=item.user_id, product_id=item.product_id, quantity=item.quantity)