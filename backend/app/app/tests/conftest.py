from typing import Dict, Generator
import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.core.config import settings
from app.db.session import client as AsyncIOMotorClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.auth import authenticate
from app.tests.utils.db import fake_db

@pytest.fixture
def event_loop():
    loop = AsyncIOMotorClient.get_io_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    return fake_db()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient, session_mocker) -> Dict[str, str]:
    session_mocker.patch('app.crud.user.authenticate', side_effect=authenticate)
    loop = AsyncIOMotorClient.get_io_loop()
    return loop.run_until_complete(get_superuser_token_headers(client))


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    loop = AsyncIOMotorClient.get_io_loop()

    return loop.run_until_complete(authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    ))
