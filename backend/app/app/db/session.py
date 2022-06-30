from app.core.config import Settings
import asyncio
import motor.motor_asyncio  # type: ignore

MONGO_URL = f"{Settings.MONGO_USER}:{Settings.MONGO_PASS}@{Settings.MONGO_HOST}:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_URL}/?authMechanism=DEFAULT")
client.get_io_loop = asyncio.get_event_loop
database = client.mongotech
