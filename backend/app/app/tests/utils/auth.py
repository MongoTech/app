from bson.objectid import ObjectId  # type: ignore


async def authenticate(db, email, password):
    if password == "wrong password":
        return None
    id = ObjectId()
    if "admin" in email:
        superuser = True
    else:
        superuser = False
    user = {"id": str(id),
            "_id": id,
            "email": email,
            "hashed_password": password,
            "is_superuser": superuser,
            "is_active": True}
    await db["users"].insert_one(document=user)
    return user


async def get_current_active_user(current_user):
    pass


async def get_current_user(db, token):
    pass
