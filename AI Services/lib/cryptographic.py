from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()

key = os.getenv("SECRET_ENCRYPTION")
chiper = Fernet(key)

def decryption_text(text: str)->str:
     decrypted = chiper.decrypt(text.encode())
     return decrypted.decode()