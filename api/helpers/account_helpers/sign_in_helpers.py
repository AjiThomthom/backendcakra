import httpx 
from fastapi import HTTPException, status
from lib.jwt import create_access_token
from lib.cookies import cookies_configuration
import bcrypt

async def SignInHelper(body, db, response):
    try:
        sign_in_payload = {
            "username" : body.username,
            "password" : body.password
        }
    
        get_accounts = await db.accounts.find_first(where={"username": sign_in_payload["username"]},include={"Profile" : True})
    
        if not get_accounts:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username atau password salah"
            )
    
        if not bcrypt.checkpw(
            body.password.encode("utf-8"),
                get_accounts.password.encode("utf-8")
                ):
                    raise HTTPException(
                        status_code=401,
                        detail="Username atau password salah"
                    )
            
        bcrypt.checkpw(sign_in_payload["password"].encode("utf-8"),get_accounts.password.encode("utf-8"))
    
        token = create_access_token({
                "id" : get_accounts.account_id,
                "username": get_accounts.username,
                "role" : get_accounts.Profile.role
        })
            
        response.set_cookie(
                **cookies_configuration(token)
                   )
            
        return {
                "message": "Success to login",
            }
    except httpx.HTTPStatusError as error:
        raise error
    except httpx.RequestError as error:
        raise error