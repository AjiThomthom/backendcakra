from fastapi import HTTPException
import httpx

async def PublicCameraHelpers(db):
    try:
        camera = await db.ccvtv.find_many(where={"category" : "PUBLIC"})

        if camera is None:
            HTTPException(detail="Camera still empty")


        return  [{
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