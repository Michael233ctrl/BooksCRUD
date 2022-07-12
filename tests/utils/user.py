from typing import Dict
from starlette.testclient import TestClient

from core.hashing import Hasher
from models.user import User


def user_authentication_headers(*, client: TestClient, username: str) -> Dict[str, str]:
    data = {"username": username, "password": "john123"}
    r = client.post(f"/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_dummy_user(db_session) -> User:
    user = User(
        username="John",
        email="john@gmail.com",
        hashed_password=Hasher.get_password_hash("john123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
