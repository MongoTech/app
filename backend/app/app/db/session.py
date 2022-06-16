import motor.motor_asyncio  # type: ignore
import asyncio

MONGODB_URL = "mongodb://admin:devpass@mongo:27017/?authMechanism=DEFAULT"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
client.get_io_loop = asyncio.get_event_loop
database = client.mongotech
