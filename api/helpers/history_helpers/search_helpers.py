from fastapi import HTTPException, status
import httpx
from datetime import datetime
import asyncio

async def SearchHelpersHistory(request, page, limit,s ,db):
    cookie = request.cookies.get("access_token")

    if cookie is None:
        raise HTTPException(detail="Access denied!")

    skip = (int(page) - 1) * int(limit)

    try:
        async def get_all_count_incident():
            return await db.incident_tragedy.count()

        async def get_all_still_pending():
            return await db.incident_tragedy.count(
                where={"status": "PENDING"}
            )

        async def get_selected_name():
            return await db.incident_tragedy.find_many(
                where={
                    "camera_name": {
                        "contains": s,
                        "mode": "insensitive",
                    }
                },
                skip=skip,
                take=limit,
                order={"created_at": "desc"},
            )

        total_count, pending_count, data = await asyncio.gather(
            get_all_count_incident(),
            get_all_still_pending(),
            get_selected_name(),
        )

        formatted_data = []

        for item in data:
            item_dict = item.dict() if hasattr(item, "dict") else dict(item)

            date_incident = item_dict.get("date_incident")

            if isinstance(date_incident, datetime):
                item_dict["time"] = date_incident.strftime("%H:%M:%S")

            elif isinstance(date_incident, str):
                try:
                    dt = datetime.fromisoformat(
                        date_incident.replace("Z", "+00:00")
                    )
                    item_dict["time"] = dt.strftime("%H:%M:%S")
                except ValueError:
                    item_dict["time"] = None

            else:
                item_dict["time"] = None

            formatted_data.append(item_dict)

        has_more = (skip + len(data)) < total_count

        return {
            "meta": {
                "total": total_count,
                "pending": pending_count,
                "page": page,
                "limit": limit,
                "has_more": has_more,
            },
            "data": formatted_data,
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    except httpx.RequestError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )