import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal, Base
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user

@pytest.fixture(scope="module")
def client():
    from app.utils.database import engine
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.mark.parametrize("email, password, expected_status", [
    ("test@example.com", "password123", 200),
    ("bad@example.com", "wrongpass", 401),
    ("duplicate@example.com", "password123", 200),
])
def test_login(client, db_session, email, password, expected_status):
    if expected_status == 200:
        # Регистрация пользователя
        create_user(db_session, UserCreate(name="Test", surname="User", email=email, password=password))

    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == expected_status