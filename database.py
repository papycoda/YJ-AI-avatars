import os
import motor.motor_asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException

MONGO_URL = "mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.avatardb

class Avatar:
    def __init__(self, _id: str, name: str, data: bytes):
        self._id = _id
        self.name = name
        self.data = data

allowed_ext = ["jpg", "jpeg", "png"]

async def fetch_all_avatars() -> list[Avatar]:
    avatars = []
    try:
        cursor = db.avatars.find({})
        async for document in cursor:
            avatars.append(Avatar(**document))
        return avatars
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_avatar(avatar: Avatar):
    try:
        if avatar.name.split(".")[-1] not in allowed_ext:
            raise HTTPException(status_code=400, detail="File extension not allowed")
        result = await db.avatars.insert_one(avatar.__dict__)
        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to create avatar")
        return avatar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_avatar(avatar_id: str, avatar: Avatar):
    try:
        result = await db.avatars.update_one({"_id": avatar_id}, {"$set": avatar.__dict__})
        if result.matched_count < 1:
            raise HTTPException(status_code=404, detail="Avatar not found")
        elif result.modified_count < 1:
            raise HTTPException(status_code=400, detail="No changes made")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_avatar(avatar_id: str):
    try:
        result = await db.avatars.delete_one({"_id": avatar_id})
        if result.deleted_count < 1:
            raise HTTPException(status_code=404, detail="Avatar not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
