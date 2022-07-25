from fastapi.testclient import TestClient
from starlette import status

DATA = {
    "title": "TEST",
    "publisher": "O'Reilly Media",
    "author": "Mark Lutz",
    "pages": "1",
    "tags": [{"name": "python"}],
}


def test_get_books(client: TestClient, user_token):
    response = client.get("/books/", headers=user_token)
    assert response.status_code == status.HTTP_200_OK


def test_get_books_by_id(client: TestClient, user_token):
    response = client.get("/books/1", headers=user_token)
    assert response.status_code == status.HTTP_200_OK


def test_create_book(client: TestClient, user_token):
    response = client.post("/books/", headers=user_token, json=DATA)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "TEST"


def test_update_books(client: TestClient, user_token):
    DATA.update({"title": "UPDATED TEST"})
    response = client.put("/books/1", headers=user_token, json=DATA)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "UPDATED TEST"


def test_update_book_if_not_exists(client: TestClient, user_token):
    DATA.update({"title": "CREATED TEST"})
    response = client.put("/books/3", headers=user_token, json=DATA)
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/books/", headers=user_token)
    assert len(response.json()) == 3


def test_delete_book(client: TestClient, user_token):
    response = client.delete("/books/1", headers=user_token)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_book_tags(client: TestClient, user_token):
    response = client.delete("/books/2/tags/", headers=user_token, json={"tagId": 1})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/books/2", headers=user_token)
    assert response.json()["tags"] == []
