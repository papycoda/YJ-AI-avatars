import os
import motor.motor_asyncio
from model import *
from fastapi import FastAPI, File, UploadFile

MONGO_URL = os.environ.get('MONGO_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URI'))

db =client.avatardb



collection = db.avatars

async def fetch_all_avatars() -> list[avatar]:
    avatars = []
    cursor = collection.find({})
    async for document in cursor:
        avatars.append(avatar(**document))
    return avatars

async def create_avatar(avatar):
    #upload image to mongodb with fastapi to create the avatar base
    avatar = await collection.insert_one(avatar)
    new_avatar = await collection.find_one({"_id": avatar.inserted_id})
    return avatar(**new_avatar)

