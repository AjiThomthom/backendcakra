from fastapi import Request, HTTPException, status, Depends
import jwt
from lib.db import db
from jose import JWTError
from datetime import datetime, timedelta, timezone
from os import getenv

SECRET_KEY = getenv("SECRET_JWT")
ALGORITMA = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60

def create_access_token(data: dict):
    payload = data.copy()

    expire  = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    payload.update({
        "exp": expire
    })

    token = jwt.encode(payload,key=SECRET_KEY,algorithm=ALGORITMA)
    return token

async def get_current_account(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token diperlukan!"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMA])
        account_id: str = payload.get("id")
        username: str = payload.get("username")

        if account_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid!"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kedaluwarsa"
        )
    
    account = await db.accounts.find_first(where={"account_id": account_id})
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Akun tidak ditemukan"
        )
    return account