from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session  # type: ignore

from app import crud, models
from app.core import security
from app.core.config import settings
from app.db.session import client, database

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        yield database
    finally:
        client.close()


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> models.User:

    try:
        if "token" not in request.cookies:
            raise ValidationError
        payload = jwt.decode(
            request.cookies["token"], settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = payload
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e

    user = await crud.user.get(db, id=token_data["sub"])  # type: ignore
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:

    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
