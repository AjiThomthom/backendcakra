from fastapi import HTTPException, status
import httpx
async def CameraDetailsHelpers(id,db):
    try:
        camera = await db.ccvtv.find_first(where={"cctv_id" : id})
    
        if camera is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kamera dengan kode {id} tidak ditemukan!"
            )
    
        return {
            "camera_name" : camera.camera_name,
            "longitude" : camera.longitude,
            "latitude" : camera.latitude,
            "location_description" : camera.location_description,
            "cctv_id" : camera.cctv_id
        }
    except httpx.HTTPStatusError as http_error:
        raise http_error
    except httpx.RequestError as error:
        raise error