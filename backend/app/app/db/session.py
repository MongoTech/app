import asyncio

import motor.motor_asyncio  # type: ignore

from app.core.config import settings

MONGO_URL = f"{settings.MONGO_USER}:{settings.MONGO_PASS}@{settings.MONGO_HOST}:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{MONGO_URL}/?authMechanism=DEFAULT"
)
client.get_io_loop = asyncio.get_event_loop
database = client.mongotech
