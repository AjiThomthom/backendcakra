from fastapi import APIRouter, HTTPException
from services.main_service import stream_camera_service

route = APIRouter()

@route.post("/offer/{id}")
async def main_watch(body : dict,id: str):
    return await stream_camera_service(body, id)