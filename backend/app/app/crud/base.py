from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from bson.objectid import ObjectId  # type: ignore
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pydantic import BaseModel
from sqlalchemy.orm import Session  # type: ignore

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: str) -> Optional[ModelType]:
        current_user = await db[self.model.__tablename__].find_one({"_id": ObjectId(id)})  # type: ignore
        if current_user:
            current_user["id"] = str(current_user["_id"])
            return current_user
        else:
            return None

    async def count(self, db: Session):
        return await db[self.model.__tablename__].count_documents({})

    async def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = []
        async for document in db[self.model.__tablename__].find().skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            result.append(document)
        return result

    async def create(self, db: Session, obj_in: dict) -> ModelType:
        data = jsonable_encoder(obj_in)
        if hasattr(obj_in, "ttl"):
            data["ttl"] = obj_in.ttl
        if hasattr(obj_in, "created"):
            data["created"] = obj_in.created
        obj = await db[self.model.__tablename__].insert_one(document=data)  # type: ignore
        user = await db[self.model.__tablename__].find_one(  # type: ignore
            {"_id": ObjectId(obj.inserted_id)}
        )  # type: ignore
        user["id"] = str(obj.inserted_id)
        return user

    async def update(
            self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in = jsonable_encoder(obj_in)

        user_id = db_obj["_id"] if db_obj["_id"] else ObjectId(db_obj["id"])
        await db[self.model.__tablename__].update_one({"_id": user_id}, {"$set": obj_in})  # type: ignore
        user = await db[self.model.__tablename__].find_one({"_id": user_id})  # type: ignore
        user["id"] = str(user["_id"])
        return user

    async def remove(self, db: AsyncIOMotorClient, id: str) -> None:
        id = ObjectId(id) if type(id) == str else id
        await db[self.model.__tablename__].delete_one({"_id": id})

