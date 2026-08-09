from fastapi import HTTPException, status
import asyncio
import httpx

async def SummaryHelpers(request,db):
    cookie = request.cookies.get("access_token")
    if cookie is None:
        raise HTTPException(detail="Access denied!",status_code=status.HTTP_403_FORBIDDEN)
    try:
        async def cctv_incident():
            return await db.incident_tragedy.find_many(take=3, order={"created_at" : "desc"})
        async def cctv_mark():
            return await db.ccvtv.find_many()
        async def cctv_public_count():
            return await db.ccvtv.count(where={
                "category" : "PUBLIC"
            })
        async def cctv_private_count():
            return await db.ccvtv.count(where={
                "category" : "PRIVATE"
            })
        async def cctv_pending_count():
            return await db.incident_tragedy.count(where={
                "status" : "PENDING"
            })

        incident,camera, public_count, private_count, pending_count = await asyncio.gather(
            cctv_incident(),cctv_mark(),cctv_public_count(),cctv_private_count(),cctv_pending_count()
        )

        return {
            "camera" : camera,
            "incident": incident,
            "count" : {
                "public" : public_count,
                "private" : private_count,
                "total": private_count + public_count,
                "pending" : pending_count
            }
        }
    except httpx.HTTPError as error:
       HTTPException(detail=error)
       raise error
    except httpx.RequestError as error:
        HTTPException(detail=error)
        raise error
        