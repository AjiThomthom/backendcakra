from typing import Optional
from lib.db import db
from fastapi import HTTPException, status, Request
from services.lib_service import get_role
from helpers.cctv_helpers.public_stream_helpers import PublicStreamHelpers
from helpers.cctv_helpers.public_camera_helpers import PublicCameraHelpers
from helpers.cctv_helpers.all_camera_map_helpers import AllCameraMapHelpers
from helpers.cctv_helpers.create_camera_helpers import CreateCameraHelpers
from helpers.cctv_helpers.camera_service_helpers import CameraServiceHelpers
from helpers.cctv_helpers.camera_detail_helpers import CameraDetailsHelpers
from helpers.cctv_helpers.delete_camera_helpers import DeleteCameraHelpers
from helpers.cctv_helpers.search_all_camera_helpers import SearchAllCamera
from helpers.cctv_helpers.update_cctv_camera_helpers import UpdateCameraCategory


async def get_public_camera_stream(id):
   return await PublicStreamHelpers(db, id)

async def get_public_camera_map():
   return await PublicCameraHelpers(db)   
    
async def get_all_camera_map_service(request):
    return await AllCameraMapHelpers(request, db)

async def get_camera_service(
    page: int = 1,
    search: Optional[str] = None,
    category: Optional[str] = None,
    request: Request = None,
):
    return await CameraServiceHelpers(request, page, category, search, db)

# Menambahkan camera CCTV baru
async def create_camera_service(body,request):
    return await CreateCameraHelpers(request, body, db)
   
# Melihat detail dari data camera CCTV 
async def get_camera_detail(id):
    return await CameraDetailsHelpers(id, db)

async def delete_camera_id(id, request):
    return await DeleteCameraHelpers(request,id,db)

async def search_cctv_name(name, request):
    return await SearchAllCamera(request,db,name)

async def update_cctv_category(category,id, request):
    return await UpdateCameraCategory(request, category,id,db)