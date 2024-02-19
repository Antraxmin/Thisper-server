from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from googleapiclient.discovery import build
import json
from connect import router as connect_router

app = FastAPI()

app.include_router(connect_router, prefix="/connect")