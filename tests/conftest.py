from typing import Generator, Any, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.base import api_router
from core.config import settings
from db.base import Base
from db.session import get_db
from tests.utils.book import create_book
from tests.utils.user import user_authentication_headers, create_dummy_user

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[TestingSessionLocal, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(app: FastAPI, db_session: TestingSessionLocal) -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = lambda: db_session
    create_book(db_session)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def user_token(client: TestClient, db_session: TestingSessionLocal) -> Dict[str, str]:
    user = create_dummy_user(db_session)
    return user_authentication_headers(client=client, username=user.username)
