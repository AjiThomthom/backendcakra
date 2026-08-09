import httpx
from fastapi import HTTPException, status
async def SearchAllCamera(request,db,name):
    cookie = request.cookies.get("access_token")
       
    if cookie is None : 
       raise httpx.HTTPStatusError(detail="Cookie not found!", status_code=status.HTTP_404_NOT_FOUND)
   
    try:
       search = await db.ccvtv.find_many(where={
           "camera_name" : {
               "contains" : name,
               "mode" : "insensitive"
           }
       })

       if search is None:
           raise httpx.HTTPStatusError(detail="Error, CCTV Not found!", status_code=status.HTTP_404_NOT_FOUND)
       
       return search
    except httpx.HTTPStatusError as http_error:
      raise HTTPException(detail=http_error)
    except httpx.RequestError as error:
      raise HTTPException(detail=error)
   
