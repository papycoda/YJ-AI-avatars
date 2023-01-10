from pydantic import BaseModel

class Picture(BaseModel):
    file: UploadFile

@router.post("/pictures/")
async def create_picture(picture: Picture):
    try:
        file_path = os.path.join("static", "pictures", picture.file.filename)
        with open(file_path, "wb") as f:
            f.write(picture.file.read())
        return {"filename": picture.file.filename}
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
            raise HTTPException(status_code=404, detail="Picture not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pictures/{filename}")
def update_picture(filename: str, picture: Picture):
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

@router.delete("/pictures/{filename}")
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
