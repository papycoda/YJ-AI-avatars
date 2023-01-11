from fastapi import APIRouter, HTTPException, File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import pathlib
import shutil
app = FastAPI()

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
async def create_avatar(avatar: Avatar):
    try:
        file_name, file_ext = os.path.splitext(avatar.file.filename)
        if file_ext.strip(".") not in allowed_ext:
            raise HTTPException(status_code=400, detail="Unsupported file extension")

        path = pathlib.Path(os.path.join("static", "pictures"))
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / avatar.file.filename
        if file_path.exists():
            raise HTTPException(status_code=409, detail="Avatar already exists")
        with file_path.open("wb") as f:
            f.write(avatar.file.read())
        return {"filename": avatar.file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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



