import pytest
from fastapi import status

def test_register_user(client, test_db):
    # Тест успешной регистрации
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    assert "hashed_password" not in response.json()


def test_register_existing_user(client, test_db):
    # Тест регистрации существующего пользователя
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already registered" in response.json()["detail"]


def test_login_success(client, test_db):
    # Тест успешного входа
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )

    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_db):
    # Тест входа с неверными учетными данными
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )

    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_logout(client, test_db):
    # Тест выхода (проверка доступа после выхода)
    # Регистрация и вход
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "is_superuser": False
        }
    )
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # Выход (в нашем случае просто проверяем, что токен больше не работает)
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверка, что токен больше не работает
    protected_response = client.get(
        "/students/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_response.status_code == status.HTTP_401_UNAUTHORIZED