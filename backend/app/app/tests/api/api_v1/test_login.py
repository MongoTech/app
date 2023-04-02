from typing import Any, Dict

import pytest  # type: ignore
from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from app.tests.utils.db import fake_db
from app.tests.utils.user import create_user
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy.orm import Session

app.dependency_overrides[get_db] = fake_db


class Storage:
    reset_password_token = None


def send_email_test(**kwargs: Any) -> None:
    if "environment" in kwargs:
        Storage.reset_password_token = kwargs["environment"]["link"].split("token=")[1]

    return None


login_data = {
    "username": settings.FIRST_SUPERUSER,
    "password": settings.FIRST_SUPERUSER_PASSWORD,
}

incorrect_login_data = {
    "username": "FIRST_SUPERUSER",
    "password": "wrong password",
}


def test_get_access_token(client: TestClient) -> None:
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_login_access_token_if_user_not_authenticated(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=incorrect_login_data
    )
    tokens = r.json()
    assert r.status_code == 400
    assert "Incorrect email or password" in tokens.values()


def test_login_access_token_if_user_not_active(client: TestClient, mocker: Any) -> None:
    mock_crud_user_is_active = mocker.patch("app.crud.user.is_active")
    mock_crud_user_is_active.return_value = False
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 400
    assert "Inactive user" in tokens.values()


def test_test_token_OK(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_recover_password_not_existing_user(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/not_existing_email@gmail.com"
    )
    tokens = r.json()
    assert r.status_code == 404
    assert (
        "The user with this username does not exist in the system." in tokens.values()
    )


def test_recover_password(client: TestClient, mocker: Any) -> None:
    mocker.patch("app.utils.send_email", side_effect=send_email_test)
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/{settings.FIRST_SUPERUSER}"
    )
    result = r.json()
    assert r.status_code == 200
    assert result["msg"] == "Password recovery email sent"


def test_reset_password_invalid_token(client: TestClient) -> None:
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": "encoded_password_reset_jwt_token",
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 400
    assert "Invalid token" in r.json().values()


@pytest.mark.asyncio
async def test_reset_password_inactive_user(
    client: TestClient, superuser_token_headers: str, db: Session, mocker: Any
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("app.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    await crud.user.update(db, db_obj=user, obj_in={"is_active": False})  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 400
    assert "Inactive user" in r.json().values()


def test_reset_password(
    client: TestClient, mocker: Any, superuser_token_headers: str
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("app.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 200
    assert {"msg": "Password updated successfully"} == r.json()


@pytest.mark.asyncio
async def test_reset_password_not_exist_user(
    client: TestClient, mocker: Any, superuser_token_headers: str, db: Session
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("app.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    await crud.user.remove(db=db, user_id=user_id)  # type: ignore
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 404
    assert {
        "detail": "The user with this username does not exist in the system."
    } == r.json()
