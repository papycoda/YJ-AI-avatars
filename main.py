from fastapi import APIRouter, HTTPException, File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from database import create_avatar, fetch_all_avatars, update_avatar, delete_avatar
#import FILersponse
from fastapi.responses import FileResponse
import os
import pathlib
import shutil

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    )

class Avatar(BaseModel):
    file: UploadFile    

allowed_ext = ["jpg", "jpeg", "png"]



@app.post("/pictures/")
async def create_picture(picture: UploadFile):
    if picture.filename.split(".")[-1] not in allowed_ext:
        raise HTTPException(status_code=400, detail="File extension not allowed")
    try:
        # create an instance of the Avatar class autogenerate id
        avatar = Avatar(file=picture)

        # call the create_avatar function from database.py
        db_response = await create_avatar(avatar)
        if db_response:
            return {"filename": picture.filename}
        else:
            raise HTTPException(status_code=500, detail="Failed to create avatar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
#get all avatars
@app.get("/pictures/")
def read_all_avatars():
    try:
        path = os.path.join("static", "pictures")
        os.makedirs(path, exist_ok=True)
        return {"filenames": ["/static/" + f for f in os.listdir(path)]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




#get avatar by filename
@app.get("/pictures/{filename}")
def read_picture(filename: str):
    file_path = os.path.join("static", "pictures", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Picture not found")


@app.put("/pictures/{filename}")
async def update_picture(filename: str, picture: UploadFile):
    if picture.filename.split(".")[-1] not in allowed_ext:
        raise HTTPException(status_code=400, detail="File extension not allowed")
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(picture.file.read())
            return {"filename": filename}
        else:
            raise HTTPException(status_code=404, detail="Picture not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@app.delete("/pictures/{filename}")
def delete_picture(filename: str):
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"filename": filename}
        else:
            raise HTTPException(status_code=404, detail="Picture not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(router)



