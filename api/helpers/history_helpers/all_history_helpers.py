from fastapi import HTTPException, status
import asyncio
from services.lib_service import date_filter
from datetime import datetime
import httpx

async def AllHistoryHelpers(request, limit, page,date, status_history, db):
   cookie = request.cookies.get("access_token")

   if cookie is None : 
        raise HTTPException(detail="ACCESS DENIED",status_code=status.HTTP_403_FORBIDDEN)

   skip = (int(page) - 1) * int(limit)

   where = {}
   try:
        async def get_all_count_incident():
           return await db.incident_tragedy.count()
                    
        async def get_all_still_pending():
           return await db.incident_tragedy.count(where={"status" : "PENDING"})

        if status_history == "all":
            print(status_history)
            async def get_all_incident():
              return await db.incident_tragedy.find_many(
                 skip=skip,
                 take=limit,
                 order={"created_at" : "desc"},
             )
                                  
            data, total_count, pending_count = await asyncio.gather(
               get_all_incident(),
               get_all_count_incident(),
               get_all_still_pending()
             ) 

        if status_history != "all":
            where["status"] = status_history.upper()
            async def get_all_incident():
              return await db.incident_tragedy.find_many(
                 skip=skip,
                 where=where,
                 take=limit,
                 order={"created_at" : "desc"},
             )
                                  
            data, total_count, pending_count = await asyncio.gather(
               get_all_incident(),
               get_all_count_incident(),
               get_all_still_pending()
             ) 

        if date == "today":
            start,end = date_filter(date)

            where["date_incident"] = {
                "gte" : start,
                "lt" : end
            }

            async def get_all_incident():
               return await db.incident_tragedy.find_many(
                  skip=skip,
                  where= where,
                  take=limit,
                  order={"created_at" : "desc"},
              )
           
            data, total_count, pending_count = await asyncio.gather(
              get_all_incident(),
              get_all_count_incident(),
              get_all_still_pending()
            )

        print(where)

        if date == "weekly":
            start,end = date_filter(date)
            where["date_incident"] = {
                "gte" : start,
                "lt" : end
            }
            async def get_all_incident():
               return await db.incident_tragedy.find_many(
                  skip=skip,
                  where= where,
                  take=limit,
                  order={"created_at" : "desc"},
              )
           
            data, total_count, pending_count = await asyncio.gather(
              get_all_incident(),
              get_all_count_incident(),
              get_all_still_pending()
            )
                        

        formatted_data = []
        for item in data:
            item_dict = item.dict() if hasattr(item, "dict") else dict(item)
            
            date_incident = item_dict.get("date_incident")
            
            if isinstance(date_incident, datetime):
                item_dict["time"] = date_incident.strftime("%H:%M:%S")
            elif isinstance(date_incident, str):
                try:
                    dt = datetime.fromisoformat(date_incident.replace("Z", "+00:00"))
                    item_dict["time"] = dt.strftime("%H:%M:%S")
                except ValueError:
                    item_dict["time"] = None
            else:
                item_dict["time"] = None

            formatted_data.append(item_dict)

        has_more = (skip + len(data)) < total_count

        return {
            "meta":{
                "total" : total_count,
                "pending" : pending_count,
                "page" : page,
                "limit" : limit,
                "has_more" : has_more
            },
            "data" : formatted_data
        }
   except httpx.HTTPStatusError as error:
        raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
   except httpx.RequestError as error:
         raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
