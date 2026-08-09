from fastapi import status, HTTPException
from services.lib_service import get_role
import httpx

async def SelectedUserHelpers(request,db,body,):
   role = get_role(request)
   if role != "OWNER":
        raise HTTPException(detail="Access denied",status_code=status.HTTP_403_FORBIDDEN)
   try:        
        user = await db.accounts.find_first(where={"account_id" : id}, include={"Profile" : True})
        await db.profile.update(data={
            "role" : body.role
        },where={"account_id" : user.account_id})
        return user
   except httpx.HTTPError as error:
        HTTPException(detail=error)
        raise error
   except httpx.RequestError as error:
        HTTPException(detail=error)
        raise error
    