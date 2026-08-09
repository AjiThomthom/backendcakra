import bcrypt
import httpx
from fastapi import HTTPException, status

async def SignUpHelpers(db, body):
    try:
        hashed_password = bcrypt.hashpw(body.password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
        payload_account = {
            "username" : body.username,
            "password":hashed_password,
        }

        account_request = await db.accounts.create(payload_account)

        if account_request is None:
            raise HTTPException(detail="Failed to create account! maybe username has been used.",
                                status_code=status.HTTP_400_BAD_REQUEST)

        payload_profile = {
            "email" : body.email,
            "fullname" : body.fullname,
            "role":body.role,
            "number_phone": body.number_phone,
            "account_id": account_request.account_id
        }

        profile_request = await db.profile.create(payload_profile)

        if profile_request is None:
            raise HTTPException(detail="Failed to create profile! something is error.",
                    status_code=status.HTTP_400_BAD_REQUEST)

        return {
            "message" : "success to register",
            "data":{
                "account" : account_request,
                "profile": profile_request
            }
        }
    except httpx.HTTPStatusError as error:
        print(error)
        raise error
    except httpx.RequestError as error:
        print(error)
        raise error
    