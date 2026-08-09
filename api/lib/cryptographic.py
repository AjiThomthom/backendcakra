from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


load_dotenv()

key = os.getenv("SECRET_ENCRYPTION").encode()

def encrypt_text(text):
    cipher = Fernet(key)
    encrypted = cipher.encrypt(text.encode())

    return encrypted.decode()
