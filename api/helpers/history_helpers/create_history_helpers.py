from fastapi import HTTPException,status
import httpx

async def CreateHistoryHelpers(body,db):
    try:
        payload = {
            "date_incident" : body.date_incident,
            "camera_name" : body.camera_name,
            "image_url" : body.image_url,
            "status" : body.status
        }

        if payload is None:
            HTTPException(detail="Payload still empty!")

        data = await db.incident_tragedy.create(payload)      

        if data is None:
            HTTPException(detail="Failed to created history!")

        return data  
    except httpx.HTTPStatusError as error:
        raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except httpx.RequestError as error:
         raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
