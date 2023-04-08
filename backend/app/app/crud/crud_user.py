from datetime import datetime
from typing import Any, Dict, Optional, TypeVar, Union

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from bson.objectid import ObjectId  # type: ignore
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

ModelType = TypeVar("ModelType", bound=Base)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db: Session, obj_in: dict) -> User:
        data = jsonable_encoder(obj_in)
        db_obj = {
            "email": data["email"],
            "full_name": data.get("full_name"),
            "is_superuser": data.get("is_superuser") or False,
            "is_active": data["is_active"],
            "created": datetime.now(),
            "access_token": data["access_token"] if "access_token" in data else "",
            "refresh_token": data["refresh_token"] if "refresh_token" in data else "",
        }
        if "password" in data:
            db_obj.setdefault("hashed_password", get_password_hash(data["password"]))
        if hasattr(obj_in, "created"):
            db_obj["created"] = obj_in.created
        obj = await db["users"].insert_one(document=db_obj)  # type: ignore
        user = await db["users"].find_one(  # type: ignore
            {"_id": ObjectId(obj.inserted_id)}
        )  # type: ignore
        user["id"] = str(obj.inserted_id)
        return user

    async def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        update_data = jsonable_encoder(obj_in)

        if "password" in update_data:  # type: ignore
            hashed_password = get_password_hash(update_data["password"])  # type: ignore
            del update_data["password"]  # type: ignore
            update_data["hashed_password"] = hashed_password  # type: ignore
        if "email" in update_data:
            del update_data["email"]  # type: ignore

        if hasattr(obj_in, "confirmed"):
            update_data["confirmed"] = obj_in.created  # type: ignore
        elif type(obj_in) == dict and "confirmed" in obj_in:
            update_data["confirmed"] = obj_in["confirmed"]

        user_id = db_obj["id"] if db_obj["id"] else ObjectId(db_obj["id"])  # type: ignore
        if not user_id:
            user_id = db_obj["_id"] if db_obj["_id"] else ObjectId(db_obj["id"])  # type: ignore
        await db["users"].update_one({"_id": user_id}, {"$set": update_data})  # type: ignore
        user = await db["users"].find_one({"_id": user_id})  # type: ignore
        user["id"] = str(user["_id"])
        return user

    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return await db["users"].find_one({"email": email})  # type: ignore

    async def authenticate(
        self, db: AsyncIOMotorClient, *, email: str, password: str
    ) -> Optional[User]:
        current_user = await self.get_by_email(db, email=email)
        if not current_user:
            return None
        if not verify_password(password, current_user["hashed_password"]):  # type: ignore
            return None
        return current_user

    @staticmethod
    def is_active(current_user: User) -> bool:
        return current_user["is_active"]  # type: ignore

    @staticmethod
    def is_superuser(current_user: User) -> bool:
        return current_user["is_superuser"]  # type: ignore


user = CRUDUser(User)
