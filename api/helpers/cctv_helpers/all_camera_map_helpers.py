import httpx 
from fastapi import HTTPException, status

async def AllCameraMapHelpers(request,db):
    cookie = request.cookies.get("access_token")
    
    if cookie is None:
            raise HTTPException(detail="Access denied, cookie not found!", status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        camera = await db.ccvtv.find_many()
    
        return [{
             "camera_name" : c.camera_name,
             "latitude" : c.latitude,
             "longitude" : c.longitude,
             "location_description" : c.location_description,
             "cctv_id" : c.cctv_id
        }
            for c in camera
        ]
    except httpx.HTTPStatusError as error:
        raise HTTPException(detail=error)
    except httpx.RequestError as error:
        raise HTTPException(detail=error)    
        