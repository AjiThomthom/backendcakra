from services.lib_service import get_role
from fastapi import HTTPException, status
import httpx

async def UpdateCameraCategory(request, category,id, db):
    role = get_role(request)
    if role == "VISITOR":
        raise HTTPException(detail="Access denied!",status_code=status.HTTP_403_FORBIDDEN)
    try:
        update_category = await db.ccvtv.update(where={"cctv_id" : id}, data={
            "category" : category.category
        })
        role = get_role(request)

        if role == "VISITOR":
            raise HTTPException(detail="Access denied!",status_code=status.HTTP_403_FORBIDDEN)

        return {
            "message": "Success updated data",
            "data": update_category
        }
    except httpx.HTTPStatusError as http_error:
       raise HTTPException(detail=http_error)
    except httpx.RequestError as error:
       raise HTTPException(detail=error)
