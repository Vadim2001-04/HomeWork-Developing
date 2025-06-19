from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.cart import CartItem
from datetime import datetime

def create_order_from_cart(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        return None

    total_price = sum(item.price * item.quantity for item in cart_items)

    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Переносим товары из корзины в заказ
    for item in cart_items:
        db.delete(item)
    db.commit()

    return new_order