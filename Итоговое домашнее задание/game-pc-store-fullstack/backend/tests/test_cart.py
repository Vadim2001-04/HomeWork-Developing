def test_add_to_cart(client):
    # Сначала создаем пользователя и товар
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "password": "password"
    }
    product_data = {
        "name": "Alienware Aurora R15",
        "description": "High-end gaming PC",
        "price": 3000,
        "rating": 4.8,
        "category_id": 1
    }

    user_response = client.post("/auth/register", json=user_data)
    product_response = client.post("/products", json=product_data)

    assert user_response.status_code == 200
    assert product_response.status_code == 200

    user_id = user_response.json()["id"]
    product_id = product_response.json()["id"]

    # Добавляем товар в корзину
    cart_response = client.post("/cart", json={"user_id": user_id, "product_id": product_id, "quantity": 2})
    assert cart_response.status_code == 200
    assert cart_response.json()["quantity"] == 2