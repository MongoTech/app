from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session  # type: ignore
import random
from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


async def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = {"username":email, "email": email, "password":password}
    return await crud.user.create(db=db, obj_in=user_in)

def create_user(client: TestClient, headers: Dict[str, str], superuser=False):
    email = f"dmitriy.golub+{random.choice(range(111111, 999999))}@gmail.com"
    password = "superpassword123"

    user_data = {
        "email": email,
        "phone": "+380932393917",
        "address": "Vita",
        "city": "kyiv",
        "zip_code": "03939",
        "is_active": True,
        "is_superuser": superuser,
        "full_name": "Dmitriy Golub",
        "password": password
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return {'username': email, "password": password}, response['id']
    return None, None

def create_user_and_login(client: TestClient, headers: Dict[str, str], superuser=False):
    login_user_data, user_id = create_user(client, headers, superuser)
    response_login = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_user_data).json()
    return {"Authorization": f"Bearer {response_login['access_token']}"}, user_id

async def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = await crud.user.create(db, obj_in=user_in_create)  # type: ignore
    else:
        user_in_update = UserUpdate(password=password)
        user = await crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
