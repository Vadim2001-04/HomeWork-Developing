from sqlalchemy.orm import Session
from app.models.cart import CartItem

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item