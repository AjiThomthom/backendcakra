from os import getenv
from dotenv import load_dotenv

load_dotenv()
enviroment = getenv("PY_ENV")


DELETE_COOKIES = {
    "key":"access_token",
    "httponly":True,
    "path":"/",
    "samesite":"lax", # Nanti ini pas production diubah jadi lax, domain nya harus sama!
    "secure": True if enviroment == "PRODUCTION" else False ,
    "domain" : ".ponpesalamin" if enviroment == "PRODUCTION" else None
}


def cookies_configuration(token):

    return {
            "key" : "access_token",
            "value" : token,
            "httponly" : True,
            "max_age" : 86400,
            "expires" : 86400,
            "path":"/",
            "domain" : ".ponpesalamin.com" if enviroment == "PRODUCTION" else None, # ini juga 
            "samesite":"lax", # Nanti ini pas production diubah jadi lax, domain nya harus sama!
            "secure": True if enviroment == "PRODUCTION" else False 
    }