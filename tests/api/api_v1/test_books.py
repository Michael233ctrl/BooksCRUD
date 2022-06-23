from fastapi.testclient import TestClient
from starlette import status


def test_create_book(client: TestClient, user_token):
    data = {
        "title": "TEST",
        "publisher": "O'Reilly Media",
        "author": "Mark Lutz",
        "pages": "1",
        "tags": ["Python", "Development", "Learning", 2009]
    }
    response = client.post("/books/", headers=user_token, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "TEST"


def test_get_books(client: TestClient, user_token):
    response = client.get('/books/', headers=user_token)
    assert response.status_code == status.HTTP_200_OK


def test_get_books_by_id(client: TestClient, user_token):
    response = client.get('/books/1', headers=user_token)
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/books/2', headers=user_token)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_books(client: TestClient, user_token):
    data = {
        "title": "UPDATED TEST",
        "publisher": "O'Reilly Media",
        "author": "Mark Lutz",
        "pages": "1",
        "tags": ["Python", "Development", "Learning", 2009]
    }
    response = client.put('/books/1', headers=user_token, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "UPDATED TEST"

    new_data = {
        "title": "CREATED TEST",
        "publisher": "O'Reilly Media",
        "author": "Mark Lutz",
        "pages": "1",
        "tags": ["Python", "Development", "Learning", 2009]
    }
    response = client.put('/books/2', headers=user_token, json=new_data)
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/books/', headers=user_token)
    assert response.json()[0]["title"] == "UPDATED TEST"
    assert response.json()[1]["title"] == "CREATED TEST"


def test_delete(client: TestClient, user_token):
    response = client.delete('/books/1', headers=user_token)
    assert response.status_code == status.HTTP_200_OK
