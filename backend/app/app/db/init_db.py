from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401


async def init_db(db) -> None:
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = {
            "email": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "is_superuser": True,
            "full_name": "Admin"
        }
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841
