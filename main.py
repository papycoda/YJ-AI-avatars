from fastapi import APIRouter, HTTPException, File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
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

async def create_upload_file(file: UploadFile):
    if file.filename.split(".")[-1] not in allowed_ext:
        raise HTTPException(status_code=400, detail="File extension not allowed")
    try:
        path = os.path.join("static", "pictures")
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, file.filename), "wb") as f:
            f.write(file.file.read()) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename }
#get all avatars

@app.get("/pictures/")
def read_all_avatars():
    try:
        path = pathlib.Path(os.path.join("static", "pictures"))
        if path.exists():
            return {"filenames": [file.name for file in path.iterdir()]}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pictures/{filename}")
def read_avatar(filename: str):
    try:
        file_path = pathlib.Path(os.path.join("static", "pictures")) / filename
        if file_path.exists():
            with file_path.open("rb") as f:
                return {"filename": filename, "data": f.read()}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pictures/{filename}")
def update_avatar_picture(filename: str, avatar: Avatar):
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
def delete_avatar_picture(filename: str):
    try:
        file_path = os.path.join("static", "pictures", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"filename": filename}
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)



