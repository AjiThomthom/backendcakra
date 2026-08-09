from fastapi import HTTPException,status
import asyncio
async def CameraServiceHelpers(request, page, category, search,db):
    cookie = request.cookies.get("access_token")
        
    if cookie is None:
        raise HTTPException(
            detail="Cookie tidak ditemukan",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    limit = 20
    offset = (int(page) - 1) * limit

    try:
            where = {}
    
            if category and category != "SEMUA":
                where["category"] = category
    
            if search:
                where["camera_name"] = {
                    "contains": search,
                    "mode": "insensitive"
                }
    
            async def public_count():
                return await db.ccvtv.count(
                    where={"category": "PUBLIC"}
                )
    
            async def private_count():
                return await db.ccvtv.count(
                    where={"category": "PRIVATE"}
                )
    
            async def total_count():
                return await db.ccvtv.count(where=where)
    
            async def fetch_data():
                return await db.ccvtv.find_many(
                    where=where,
                    skip=offset,
                    take=limit,
                    order={"cctv_id": "desc"}
                )
    
            public, private, total_data, data = await asyncio.gather(
                public_count(),
                private_count(),
                total_count(),
                fetch_data()
            )
    
            return {
                "data": data,
                "meta":{
                "page": page,
                "limit": limit,
                "total_data": total_data,
                "total_page": (total_data + limit - 1) // limit,
                "public": public,
                "private": private,
                }
            }
    
    except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            ) 
    