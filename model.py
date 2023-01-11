from pydantic import BaseModel
from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os

router = APIRouter()

class Avatar(BaseModel):
    file: UploadFile




