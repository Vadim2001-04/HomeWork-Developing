import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal, engine
from app.models.user import User
from app.models.product import Product
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.crud.product import create_product

@pytest.fixture(scope="module")
def client():
    from app.utils.database import Base
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_order_as_user(client):
    # Создаем пользователя и товар
    db = SessionLocal()
    user = create_user(db, UserCreate(name="Test", surname="User", email="user@example.com", password="password"))
    product = create_product(db, {
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    })
    db.close()

    login = client.post("/auth/login", json={"email": "user@example.com", "password": "password"})
    token = login.json()["access_token"]

    response = client.post("/orders", json={
        "items": [{"product_id": product.id, "quantity": 2}]
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "order_id" in response.json()