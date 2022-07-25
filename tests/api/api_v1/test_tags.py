from fastapi.testclient import TestClient
from starlette import status


def test_get_tags(client: TestClient, user_token):
    response = client.get("/tags/", headers=user_token)
    assert response.status_code == status.HTTP_200_OK


def test_update_tags(client: TestClient, user_token):
    response = client.put("/tags/1", headers=user_token, json={'name': "Python"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Python'


def test_delete_tags(client: TestClient, user_token):
    response = client.delete("/tags/1", headers=user_token)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() == 'Success!'
    response = client.get("/tags/", headers=user_token)
    assert response.json() == []
