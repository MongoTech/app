from typing import Any, Optional
from unittest.mock import MagicMock

from app.core.config import settings
from app.core.security import get_password_hash
from bson.objectid import ObjectId  # type: ignore
from sqlalchemy.orm import Session

first_user_id = ObjectId()


class MongoDbTest(MagicMock):
    users = {}  # type: ignore

    def __init__(self, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        user = {
            "id": str(first_user_id),
            "_id": first_user_id,
            "email": settings.FIRST_SUPERUSER,
            "hashed_password": get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            "is_superuser": True,
            "is_active": True,
        }
        self.users.setdefault(str(first_user_id), user)

    async def find_one(self, find: dict) -> Optional[dict]:
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    return self.users[user]
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    return self.users[user]
        return None

    async def insert_one(self, document: dict) -> Optional[type]:
        if "email" not in document:
            return None

        user_id = ObjectId() if "_id" not in document else document["_id"]
        document["id"] = str(user_id)
        document["_id"] = user_id

        user = self.users.setdefault(document["id"], document)

        user_obj = type("User", (), user)
        setattr(user_obj, "inserted_id", user_id)
        setattr(user_obj, "_id", user_id)
        return user_obj

    async def update_one(self, find: dict, update: dict) -> Optional[dict]:
        current_user = None
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user

        if current_user in self.users:
            for field in update["$set"]:
                self.users[current_user][field] = update["$set"][field]
            return self.users[current_user]
        return None

    async def delete_one(self, find: dict) -> None:
        current_user = None
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user
        if current_user in self.users:
            del self.users[current_user]
        pass


db = None


def fake_db() -> Session:
    global db
    if not db:
        db = MongoDbTest()
    return db
