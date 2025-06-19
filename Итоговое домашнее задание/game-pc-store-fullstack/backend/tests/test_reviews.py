import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.product import Product
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.crud.product import create_product

@pytest.fixture(scope="function")
def setup_product_and_user():
    db = SessionLocal()
    user = create_user(db, UserCreate(name="Test", surname="User", email="test@example.com", password="password"))
    product = create_product(db, {
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    })
    db.close()
    return {"user": user, "product": product}

def test_add_review(setup_product_and_user):
    db = SessionLocal()
    user = setup_product_and_user["user"]
    product = setup_product_and_user["product"]
    db.close()

    login = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    token = login.json()["access_token"]

    review_data = {
        "user_id": user.id,
        "product_id": product.id,
        "text": "Отличный ПК!"
    }

    response = client.post("/reviews", json=review_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["text"] == "Отличный ПК!"