from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from os import getenv


SECRET_KEY = getenv("SECRET_JWT")

def get_role(request):
    cookie = request.cookies.get("access_token")

    if cookie is None:
        raise HTTPException(detail="Acces denied!, Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    data = jwt.decode(key=SECRET_KEY,jwt=cookie,algorithms=["HS256"])
    role = data["role"]

    return role

def date_filter(type):
    if type == "today":
        today = datetime.now(timezone.utc).date()
    
        start = datetime.combine(today, datetime.min.time(),tzinfo=timezone.utc)
        end = start + timedelta(days = 1)

    if type == "weekly":
        today = datetime.now(timezone.utc)

        start = (today - timedelta(days=today.weekday())).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )    

        end = start + timedelta(days = 7)


    return start, end 