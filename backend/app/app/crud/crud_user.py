from typing import Any, Dict, Optional, Union, TypeVar, List
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.db.base_class import Base
ModelType = TypeVar("ModelType", bound=Base)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get(self, db: Session, id: str) -> Optional[ModelType]:
        current_user = await db["users"].find_one({"_id": ObjectId(id)})
        if current_user:
            current_user['id'] = str(current_user['_id'])
            return current_user
        else:
            return None

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = []
        async for document in db["users"].find().skip(skip).limit(limit):
        # async for document in db["users"].find():
            document["id"] = str(document['_id'])# noqa
            result.append(document)
        return result

    async def get_by_email(self, db, email: str) -> Optional[User]:
        return await db["users"].find_one({"email": email}) # noqa

    async def create(self, db, obj_in: dict) -> User:
        obj_in = jsonable_encoder(obj_in)
        db_obj = {
            "email": obj_in["email"],
            "hashed_password": get_password_hash(obj_in["password"]),
            "full_name": obj_in.get("full_name"),
            "is_superuser": obj_in.get("is_superuser") or False,
            "is_active": True
        }
        obj = await db["users"].insert_one(document=db_obj) # noqa
        user = await db["users"].find_one({"_id": ObjectId(obj.inserted_id)}) # noqa
        user["id"] = str(obj.inserted_id)
        return user

    async def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        obj_in = jsonable_encoder(obj_in)
        update_data = obj_in

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if 'email' in update_data:
            del update_data['email']
        await db["users"].update_one({"_id": ObjectId(db_obj['id'])},{'$set': update_data}) # noqa
        user =  await db["users"].find_one({"_id":  ObjectId(db_obj['id'])}) # noqa
        user["id"] = str(user["_id"])
        return user

    async def authenticate(self, db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[User]:
        current_user = await self.get_by_email(db, email=email)
        if not current_user:
            return None
        if not verify_password(password, current_user["hashed_password"]):
            return None
        return current_user

    @staticmethod
    def is_active(current_user: User) -> bool:
        return current_user["is_active"]

    @staticmethod
    def is_superuser(current_user: User) -> bool:
        return current_user["is_superuser"]


user = CRUDUser(User)
