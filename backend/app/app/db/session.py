import asyncio

import motor.motor_asyncio  # type: ignore

MONGODB_URL = "mongodb://root:mongo@localhost:27017/?authMechanism=DEFAULT"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
client.get_io_loop = asyncio.get_event_loop
database = client.mongotech
