from typing import Any
from unittest.mock import MagicMock

from bson.objectid import ObjectId  # type: ignore

from app.core.config import settings

first_user_id = ObjectId()


class MongoDbTest(MagicMock):
    users = {}  # type: ignore

    def __init__(self, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        user = {
            "id": str(first_user_id),
            "_id": first_user_id,
            "email": settings.FIRST_SUPERUSER,
            "hashed_password": "$2b$12$mLRl07VnztvwkE36I0kC1uLiwalJ39mew.A2PKc1g0MRkf1AtdGD6",
            "is_superuser": True,
            "is_active": True,
        }
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
        # for user in self.users:
        #     if document["email"] == self.users[user]["email"]:
        #         user_obj = type("User", (), self.users[user])
        #         user_obj.inserted_id = self.users[user]["id"]
        #         setattr(user_obj, "_id", self.users[user]["id"])
        #         return user_obj

        if "email" in document:
            if "_id" not in document:
                id = ObjectId()
            else:
                id = document["_id"]
            document["id"] = str(id)
            document["_id"] = id

            user = self.users.setdefault(document["id"], document)

            user_obj = type("User", (), user)
            user_obj.inserted_id = id
            setattr(user_obj, "_id", id)
            return user_obj

    async def update_one(self, find, update):
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user
        for field in update["$set"]:
            self.users[current_user][field] = update["$set"][field]
            pass

    async def delete_one(self, find):
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user
        del self.users[current_user]
        pass


db = None


def fake_db():
    global db
    if not db:
        db = MongoDbTest()
    return db
