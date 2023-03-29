from typing import Any, List

from starlette.status import HTTP_302_FOUND
import math
from app.core import security
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime, timedelta
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email, create_confirmation_token


router = APIRouter()


@router.get("/pagination")
async def pagination(
    per_page=10,
    db: Session = Depends(deps.get_db),
) -> Any:
    count = await crud.user.count(db=db)
    return math.ceil(count/per_page)


@router.get("/activate", response_model=Any)
async def activate(
    token: str,
    response: Response,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    confirm = await crud.confirm.get_by_token(db=db, token=token)
    user_in = {
        "confirmed": datetime.now(),
        "email": confirm["email"],
        "is_active": True
    }
    user = await crud.user.get(db=db, id=confirm["user_id"])
    await crud.user.update(db=db, db_obj=user, obj_in=user_in)
    await crud.confirm.remove(db=db, id=confirm["_id"])
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="token", value=security.create_access_token(
            user["_id"], expires_delta=access_token_expires  # type: ignore
        ), expires=access_token_expires)
    headers = {"Location": "/dashboard"}
    raise HTTPException(status_code=HTTP_302_FOUND, headers=headers)


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(db, skip=skip, limit=limit)  # type: ignore
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=jsonable_encoder(user_in))
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user["_id"] = str(current_user["_id"])  # type: ignore
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    return await crud.user.update(db, db_obj=current_user, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/stats", response_model=Any)
async def stat(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Retrieve users.
    """
    return {
        "users": await crud.user.count(db=db)
    }


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, id=user_id)  # type: ignore
    if user["email"] == current_user["email"]:  # type: ignore
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db, id=user_id)  # type: ignore
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)  # type: ignore
    return user


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user_in.is_superuser = False
    user_in.is_active = False
    user = await crud.user.create(db, obj_in=user_in)
    await create_confirmation_token(db, user, user["email"])
    return user


@router.delete("/{id}", response_model=schemas.User)
async def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> schemas.User:
    """
    Delete an quota_room.
    """
    if id == 1:
        raise HTTPException(status_code=403, detail="You can't delete superuser")

    user = await crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exists")

    await crud.user.remove(db=db, id=id)
    return user
