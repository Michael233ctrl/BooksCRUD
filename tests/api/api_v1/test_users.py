from starlette import status


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "John Doe",
            "email": "john@example.com",
            "password": "johndoe123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["email"] == "john@example.com"
