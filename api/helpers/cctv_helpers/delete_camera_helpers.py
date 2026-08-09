from services.lib_service import get_role
from fastapi import HTTPException, status
import httpx

async def DeleteCameraHelpers(request,id,db):
    role = get_role(request)

    if role not in ("STAFF","OWNER"):
        raise HTTPException(detail="Acess denied", status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        psql = await db.ccvtv.delete(where={"cctv_id" : id})
        
        if psql is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kamera dengan kode {id} tidak ditemukan!"
            )
        
        return {
            "message" : "Berhasil menghapus camera",
            "data": psql
        }
    except httpx.HTTPStatusError as http_error:
        raise http_error
    except httpx.RequestError as error:
        raise error
