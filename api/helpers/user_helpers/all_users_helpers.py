from fastapi import HTTPException, status
import httpx

async def AllUsersHelpers(request, db):
    cookie = request.cookies.get("access_token")

    if cookie is None : 
       raise HTTPException(detail="Cookie not found!",status_code=status.HTTP_404_NOT_FOUND)

    try:
        allUsers = await db.accounts.find_many(include={'Profile' : True})

        print(allUsers)
        return allUsers
    except httpx.HTTPError as error:
        HTTPException(detail=error)
        raise error
    except httpx.RequestError as error:
        HTTPException(detail=error)
        raise error
