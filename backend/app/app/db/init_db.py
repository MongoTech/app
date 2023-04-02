from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.db import base  # noqa: F401
from app.schemas.user import UserCreate


async def init_db(db: Session) -> None:
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_active=True,
            full_name="Admin",
        )
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841
