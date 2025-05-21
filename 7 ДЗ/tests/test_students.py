import pytest
from fastapi import status


def test_create_student_success(client, test_db):
    # Создаем суперпользователя
    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass",
            "is_superuser": True
        }
    )

    # Логинимся
    login_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_response.json()["access_token"]

    # Создаем студента
    response = client.post(
        "/students/",
        json={
            "last_name": "Иванов",
            "first_name": "Иван",
            "faculty": "АВТФ",
            "course": "Информатика",
            "grade": 85.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["last_name"] == "Иванов"
    assert response.json()["grade"] == 85.0


def test_create_student_unauthorized(client, test_db):
    # Попытка создать студента без авторизации
    response = client.post(
        "/students/",
        json={
            "last_name": "Иванов",
            "first_name": "Иван",
            "faculty": "АВТФ",
            "course": "Информатика",
            "grade": 85.0
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_students_success(client, test_db):
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

    # Получение списка студентов
    response = client.get(
        "/students/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_all_students_unauthorized(client, test_db):
    # Попытка получить список студентов без авторизации
    response = client.get("/students/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_student_success(client, test_db):
    # Создаем суперпользователя
    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass",
            "is_superuser": True
        }
    )

    # Логинимся
    login_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_response.json()["access_token"]

    # Создаем студента
    create_response = client.post(
        "/students/",
        json={
            "last_name": "Иванов",
            "first_name": "Иван",
            "faculty": "АВТФ",
            "course": "Информатика",
            "grade": 85.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    student_id = create_response.json()["id"]

    # Удаляем студента
    delete_response = client.delete(
        f"/students/{student_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что студент удален
    get_response = client.get(
        f"/students/{student_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND