from unittest.mock import MagicMock
from bson.objectid import ObjectId  # type: ignore
from app.core.config import settings
from typing import Any
first_user_id = ObjectId()
class MongoDbTest(MagicMock):
    users = {}  # type: ignore

    def __init__(self, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        user = {str(first_user_id): str(first_user_id),
                "_id": first_user_id,
                "email": settings.FIRST_SUPERUSER,
                "hashed_password": "$2b$12$mLRl07VnztvwkE36I0kC1uLiwalJ39mew.A2PKc1g0MRkf1AtdGD6",
                "is_superuser": True,
                "is_active": True}
        self.users.setdefault(str(first_user_id), user)

    async def find_one(self, find):
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    return self.users[user]
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    return self.users[user]
        return None

    def skip(self):
        pass

    async def find(self):
        yield self.users

    async def insert_one(self, document):
        if "email" in document:
            if "_id" not in document:
                id = ObjectId()
            else:
                id = document["_id"]
            document["id"] = str(id)
            document["_id"] = id

            user = self.users.setdefault(document["id"], document)

            user_obj = type('User', (), user)
            user_obj.inserted_id = id
            setattr(user_obj, "_id", id)
            return user_obj

    async def update_one(self, where, update):
        pass


db = None


def fake_db():
    global db
    if not db:
        db = MongoDbTest()
    return db
