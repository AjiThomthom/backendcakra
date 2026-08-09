from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from router.main_route import route
from lib.db import db
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print("berhasil terhubung ke database")
    
    yield
    
    await db.disconnect()
    print("database berhasil diputus")

app = FastAPI(lifespan=lifespan)

# 1. Daftar domain yang secara pasti diizinkan
allowed_origins = [
    "https://cakra.ponpesalamin.com",
    "http://localhost:3000"
]

# 2. Ambil dari .env dan bersihkan garis miring di akhir (jika ada)
production_url = os.getenv("WEB_URL_LOCAL")
if production_url:
    cleaned_url = production_url.rstrip("/")
    allowed_origins.append(cleaned_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(route, prefix="/stream/v1.0")
