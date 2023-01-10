from fastapi import APIRouter, HTTPException, File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )

