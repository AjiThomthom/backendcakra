from services.lib_service import get_role
from fastapi import HTTPException, status
from datetime import datetime, timezone
from lib.cryptographic import encrypt_text
import httpx

async def CreateCameraHelpers(request,body,db):
    role = get_role(request)
    if role not in ("STAFF", "OWNER"):
        raise HTTPException(detail="Acess denied", status_code=status.HTTP_403_FORBIDDEN)
    
    try:

        encrypted_url = encrypt_text(body.source_url)

        payload = {
            "camera_name" : body.camera_name,
            "source_url" : encrypted_url,
            "latitude" : body.latitude,
            "longitude" : body.longitude,
            "category" : body.category,
            "location_description" : body.location_description,
            "created_at" : datetime.now(timezone.utc)
        }

        psql = await db.ccvtv.create(data=payload)

        return {
            "message" : "Berhasil menambahkan camera",
            "data": psql
        }
    except httpx.HTTPStatusError as error:
        print(error)
        raise HTTPException(detail=error)
    except httpx.RequestError as error:
        print(error)
        raise HTTPException(detail=error)
