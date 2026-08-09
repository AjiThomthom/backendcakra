from typing import Optional
from fastapi import APIRouter, Response, Depends, Request, Query
from lib.jwt import get_current_account
from router import cctv_router as CCTV
from schema.account_schema import AccountModel, ProfileModel, RegisterProfile, UpdateProfileModel
from schema.data_history_schema import HistoryModel, HistoryStatusUpdateModel
import services.data_history_service as HistoryServices
import services.main_service as Services
import services.cctv_service as CCTVService
import services.account_service as AccountService

router = APIRouter()


# Get Summary data
@router.get('/home')
async def get_summary_data(request: Request, account = Depends(get_current_account)):
    return await Services.get_summary_data(request)

# Cari data berdasarkan nama kamera
@router.get('/data-history/search')
async def get_search_name(
        request: Request,
        s : Optional[str] = None,
        page:int=Query(default=1,ge=1),
        limit  : int = Query(default=20,ge=1,le=100),
        account = Depends(get_current_account)
        ):
    return await HistoryServices.get_search_name(request,s,page,limit)


@router.get("/data-history",summary="Mengambil semua data dari database")
async def get_all_data_history(request : Request,status : str = "all",date:str = "all",page: int = Query(default=1, ge=1),limit  : int = Query(default=20,ge=1,le=100), account = Depends(get_current_account)):
    return await HistoryServices.get_all_history(request,status,date,page,limit)

@router.post("/data-history",summary="Menambah data history")
async def create_data_history(body : HistoryModel):
    return await HistoryServices.created_history(body)

@router.patch("/data-history",summary="Mengubah status")
async def update_status_data_history(request: Request,body : HistoryStatusUpdateModel, id: str, account = Depends(get_current_account)):
    return await HistoryServices.update_history(request,body,id)

# Users Data

@router.get("/users/search")
async def search_user_one(request: Request,s: Optional[str] = None, account = Depends(get_current_account)):
    return await Services.search_user(username=s,request=request)

@router.get("/users")
async def all_users(request: Request,account = Depends(get_current_account)):
    return await Services.get_all_users(request)


@router.patch("/users/{id}")
async def update_user(id,body : UpdateProfileModel, request: Request, account = Depends(get_current_account)):
    return await Services.update_selected_users(id,body, request)

# Authentication Router
@router.post("/account/login")
async def sign_in(body : AccountModel, response: Response):
    return await AccountService.sign_in_account(body, response)

@router.post("/account/register")
async def create_account(body : RegisterProfile ):
    return await AccountService.create_account(body)

@router.delete("/account/logout")
async def delete_cookie(response:Response, account = Depends(get_current_account)):
    return await AccountService.sign_out_account(response)

# Data kekerasan dari layanan eksternal & database
@router.get("/violance")
async def get_violance():
    return await Services.get_violance_service()

@router.post("/violance")
async def add_vioalance():
    return {"Hello" : "Hello"}

@router.patch("/violance")
async def update_status():
    return { "Hello": "Hello"}


# Komunikasi web-socket
@router.websocket("/ws/camera")
async def camera_strem():
    print("streaming start")