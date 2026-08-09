import httpx 
from fastapi import HTTPException, status
async def PublicStreamHelpers(db,id):
    try:
        camera = await db.ccvtv.find_first(where={"cctv_id" : id, "category" : "PUBLIC"})

        if camera is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kamera dengan kode {id} tidak ditemukan!"
        )
        return{
                "camera_name" : camera.camera_name,
                "latitude" : camera.latitude,
                "longitude" :  camera.longitude,
                "location_description" : camera.location_description,
                "cctv_id" : camera.cctv_id
            }
    except httpx.HTTPStatusError as http_error:
        raise http_error
    except httpx.RequestError as error:
        raise error    