from typing import Any, TypeVar

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.confirm import Confirm
from app.schemas.confirm import ConfirmCreate, ConfirmUpdate
from sqlalchemy.orm import Session  # type: ignore

ModelType = TypeVar("ModelType", bound=Base)


class CRUDConfirm(CRUDBase[Confirm, ConfirmCreate, ConfirmUpdate]):
    async def get_by_token(self, db: Session, token: str) -> Any:
        return await db["confirm"].find_one({"token": token})  # type: ignore


confirm = CRUDConfirm(Confirm)
