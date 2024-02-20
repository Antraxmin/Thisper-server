from fastapi import FastAPI
from googleapiclient.discovery import build
from api.connect import router as connect_router

app = FastAPI()

app.include_router(connect_router, prefix="/connect")