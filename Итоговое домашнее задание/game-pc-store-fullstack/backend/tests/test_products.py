import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal, engine
from app.models.base import Base
from app.models.product import Product

# Создаем тестовую БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def client():
    from app.utils.database import Base
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_product(client):
    response = client.post("/products", json={
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alienware Aurora R15"
    assert data["price"] == 3000