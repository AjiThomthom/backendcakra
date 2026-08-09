from pydantic import Field, BaseModel
from datetime import datetime

class HistoryModel(BaseModel):
    date_incident : datetime = Field(default=datetime.now())
    camera_name : str 
    image_url : str
    status: str

class HistoryStatusUpdateModel(BaseModel):
    status : str
