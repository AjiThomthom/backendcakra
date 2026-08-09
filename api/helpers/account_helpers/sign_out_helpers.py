from lib.cookies import DELETE_COOKIES
import httpx
async def SignOutHelpers(response):
    try:
        response.delete_cookie(
            **DELETE_COOKIES
       )

        return {
        "message": "Success to logout"
        }
    except httpx.HTTPStatusError as error:
        print(error)
        raise error
    except httpx.RequestError as error:
        print(error)
        raise error
    