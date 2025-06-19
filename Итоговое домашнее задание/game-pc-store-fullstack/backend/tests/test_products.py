import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_product_as_admin(client):
    # Создаем админа
    db = SessionLocal()
    admin = create_user(db, UserCreate(name="Admin", surname="User", email="admin@example.com", password="password", role="admin"))
    db.close()

    login = client.post("/auth/login", json={"email": "admin@example.com", "password": "password"})
    token = login.json()["access_token"]

    product_data = {
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    }

    response = client.post("/products", json=product_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["name"] == "Alienware Aurora R15"

def test_create_product_as_user_fails(client):
    # Создаем обычного пользователя
    db = SessionLocal()
    user = create_user(db, UserCreate(name="Test", surname="User", email="user@example.com", password="password"))
    db.close()

    login = client.post("/auth/login", json={"email": "user@example.com", "password": "password"})
    token = login.json()["access_token"]

    product_data = {
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    }

    response = client.post("/products", json=product_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403