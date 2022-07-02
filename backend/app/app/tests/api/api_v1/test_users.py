from typing import Dict

import pytest  # type: ignore
from fastapi.testclient import TestClient
from jose import jwt  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import crud
from app.api.deps import get_db
from app.core import security
from app.core.config import settings
from app.main import app
from app.schemas.user import UserCreate
from app.tests.utils.db import fake_db
from app.tests.utils.user import create_user_and_login
from app.tests.utils.utils import random_email, random_lower_string

app.dependency_overrides[get_db] = fake_db


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True


@pytest.mark.asyncio
async def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = await crud.user.get_by_email(db, email=username)
    assert user
    assert user["email"] == created_user["email"]  # type: ignore


@pytest.mark.asyncio
async def test_update_current_user(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user_header, _ = create_user_and_login(client, superuser_token_headers)
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password, "full_name": "User name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=user_header,
        json=data,
    )
    assert 200 == r.status_code


@pytest.mark.asyncio
async def test_update_current_user_by_me(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user = await crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    data = {"email": "me@example.com", "password": "password", "full_name": "User name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/{user['id']}",  # type: ignore
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 == r.status_code


@pytest.mark.asyncio
async def test_update_current_user_by_me_does_not_exist(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user = await crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    data = {"email": "me@example.com", "password": "password", "full_name": "User name"}
    await crud.user.remove(db=db, user_id=user["id"])  # type: ignore
    r = client.put(
        f"{settings.API_V1_STR}/users/{user['id']}",  # type: ignore
        headers=superuser_token_headers,
        json=data,
    )
    assert 404 == r.status_code


@pytest.mark.asyncio
async def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    user_id = user["_id"]  # type: ignore
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user["email"] == api_user["email"]  # type: ignore


@pytest.mark.asyncio
async def test_get_existing_user_super(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    r = client.get(
        f"{settings.API_V1_STR}/users/{user['id']}",  # type: ignore
        headers=superuser_token_headers,
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_user_super_no_access(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user_header, user_id = create_user_and_login(client, superuser_token_headers)
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    r = client.get(
        f"{settings.API_V1_STR}/users/{user['id']}",  # type: ignore
        headers=user_header,
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    await crud.user.create(db, obj_in=user_in)  # type: ignore
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def notest_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    await crud.user.create(db, obj_in=user_in)  # type: ignore

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    await crud.user.create(db, obj_in=user_in2)  # type: ignore

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": "Bearer invalid token"},
    )
    assert 403 == r.status_code


@pytest.mark.asyncio
async def test_get_current_user_user_not_found(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user_headers_auth, user_id = create_user_and_login(client, superuser_token_headers)

    token = user_headers_auth["Authorization"].split(" ")[1]

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
    await crud.user.remove(db=db, user_id=payload["sub"])
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=user_headers_auth)
    assert 404 == r.status_code


@pytest.mark.asyncio
async def test_get_current_user_user_not_active(
    client: TestClient, superuser_token_headers: str, db: Session
) -> None:
    user_headers_auth, user_id = create_user_and_login(client, superuser_token_headers)

    token = user_headers_auth["Authorization"].split(" ")[1]

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
    db.users[payload["sub"]]["is_active"] = False  # type: ignore
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=user_headers_auth)
    assert 400 == r.status_code
