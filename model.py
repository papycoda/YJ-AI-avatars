from pydantic import BaseModel
from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os

router = APIRouter()

class Avatar(BaseModel):
    file: UploadFile

@router.post("/pictures/")
async def create_picture(avatar: Avatar):
    try:
        file_path = os.path.join("static", "pictures", avatar.file.filename)
        with open(file_path, "wb") as f:
            f.write(avatar.file.read())
        return {"filename": avatar.file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pictures/{filename}")
def read_picture(filename: str):
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return {"filename": filename, "data": f.read()}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pictures/{filename}")
def update_picture(filename: str, avatar: Avatar):
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(avatar.file.read())
            return {"filename": filename}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/pictures/{filename}")
def delete_picture(filename: str):
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"filename": filename}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
