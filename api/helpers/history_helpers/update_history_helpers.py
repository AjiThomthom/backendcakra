from services.lib_service import get_role
from fastapi import HTTPException, status
import httpx

async def UpdateHistoryHelpers(request,body,db,id):
    role = get_role(request)

    if role == "VISITOR":
        raise HTTPException(detail="Access denied!",status_code=status.HTTP_403_FORBIDDEN)

    try:
        payload = {
            "status" : body.status
        }

        if payload is None:
            HTTPException(detail="Payload still empty!")

        data = await db.incident_tragedy.update(where={
            "incident_id" : id
        },data=payload)

        return data
    except httpx.HTTPStatusError as error:
        raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except httpx.RequestError as error:
         raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
