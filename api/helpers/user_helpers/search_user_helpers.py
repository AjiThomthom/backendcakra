from fastapi import HTTPException, status
import httpx

async def SearchUserHelpers(request, username,db):
    cookie = request.cookies.get("access_token")

    if cookie is None : 
       raise HTTPException(detail="Cookie not found!",status_code=status.HTTP_404_NOT_FOUND)
   
    if username is None:
        raise HTTPException(detail="Username must been filled!",status_code=status.HTTP_400_BAD_REQUEST)
    try:
        data = await db.accounts.find_many(where={
            "OR" : [
                {"username" : {
                    "contains" : username,
                    "mode" : "insensitive"
                }},
                {"Profile": {
                    "is":{
                        "fullname" : {
                            "contains" : username,
                            "mode" : "insensitive"
                        }
                    }
                }}
            ]
        },include={
            "Profile" : True
        })

        if data is None : 
            raise HTTPException(detail="User not found!",status_code=status.HTTP_404_NOT_FOUND)

        return data
    except httpx.HTTPStatusError as error:
        HTTPException(detail=error)
        raise error
    except httpx.RequestError as error:
        HTTPException(detail=error)
        raise error