from fastapi import FastAPI,APIRouter,Depends
from helper.config import get_settings,Settings
import os


base_router = APIRouter()

@base_router.get("/")
async def welcome(app_settings:Settings =Depends(get_settings)):
    app_settings = get_settings()
    app_name =app_settings.APP_NAME
    app_version =app_settings.APP_VERSION


    return {
        "app name :":app_name,
        "app version :":app_version,
    }
