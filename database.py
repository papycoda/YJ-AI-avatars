import os
import motor.motor_asyncio
from model import *

MONGO_URL = os.environ.get('MONGO_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URI'))

db =client.avatardb

collections = db.avatars

async def fetch_all_avatars() -> list[avatars]:
    avatars = []
    cursor = collection.find({})
    async for document in cursor:
        avatars.append(avatar(**document))
    return avatars
