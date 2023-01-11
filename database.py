import os
import motor.motor_asyncio
from model import *
from fastapi import FastAPI, File, UploadFile

MONGO_URL = os.environ.get('MONGO_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URI'))

db =client.avatardb



collection = db.avatars

async def fetch_all_avatars() -> list[Avatar]:
    avatars = []
    cursor = collection.find({})
    async for document in cursor:
        avatars.append(Avatar(**document))
    return avatars

async def create_avatar(avatar):
    #upload image to mongodb with fastapi to create the avatar base
    avatar = await collection.insert_one(avatar)
    new_avatar = await collection.find_one({"_id": avatar.inserted_id})
    return avatar(**new_avatar)

async def update_avatar(avatar_id, data):
    #update the avatar base with new image
    if len(data) < 1:
        return False
    avatar = await collection.find_one({"_id": avatar_id})
    if avatar:
        updated_avatar = await collection.update_one(
            {"_id": avatar_id}, {"$set": data}
        )
        if updated_avatar:
            return True
        return False

async def delete_avatar(avatar_id):
    avatar = await collection.find_one
    if avatar:
        await collection.delete_one({"_id": avatar_id})
        return True



