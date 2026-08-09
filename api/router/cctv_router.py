from fastapi import APIRouter, Depends, Request
from typing import Optional
from lib.jwt import get_current_account
from schema.cctv_schema import CCTVCreate, CCTVUpdate
from services import cctv_service as CCTVService
cctv = APIRouter()

@cctv.get("/cctvs/public/{id}")
async def cctv_public_stream(id):
    return await CCTVService.get_public_camera_stream(id)

@cctv.get("/cctvs/public")
async def cctv_public():
    return await CCTVService.get_public_camera_map()

@cctv.get("/cctvs/all")
async def cctv_list(request: Request ,account = Depends(get_current_account)):
    return await CCTVService.get_all_camera_map_service(request)

@cctv.get("/cctvs", summary="Mengambil semua CCTV dari database")
async def get_camera_list(page:str,search : Optional[str] = None, category : Optional[str] = None,request:Request = None,account = Depends(get_current_account)):
    return await CCTVService.get_camera_service(page,search,category,request)

@cctv.patch("/cctvs/{id}", summary="Mengupdate kategori cctv")
async def update_camera_category(category : CCTVUpdate,id,request: Request, account=Depends(get_current_account)):
    return await CCTVService.update_cctv_category(category,id,request)

@cctv.post("/cctvs", summary="Menambahkan cctv baru ke sistem")
async def  add_camera(body : CCTVCreate, request: Request,account=Depends(get_current_account)):
    return  await CCTVService.create_camera_service(body,request)

@cctv.get("/cctvs/{id}", summary="Melihat detail dari cctv")
async def  get_detail_camera(id,account=Depends(get_current_account)):
    return  await CCTVService.get_camera_detail(id)

@cctv.delete("/cctvs/{id}")
async def  delete_camera_id(id, request: Request,account=Depends(get_current_account)):
    return await CCTVService.delete_camera_id(id, request)
