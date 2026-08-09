from pydantic import BaseModel, Field
from typing import Optional

class CCTVCreate(BaseModel):
    camera_name : str = Field(...,examples=["Kamera depan toko"])
    source_url : str = Field(...,examples=["rtsp://192.168.1.100/stream1"])
    latitude : float = Field(None, examples=[-6.2088])
    longitude : float = Field(None, examples=[106.8456])
    category : str = Field(...,example=["PRIVATE","PUBLIC"])
    location_description: Optional[str] = Field(None, examples=["Gerbang utama perumahan Kerta Mukti blok C"])

class CCTVUpdate(BaseModel):
    category : str = Field(...)