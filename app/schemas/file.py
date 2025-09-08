# app/schemas/file.py
from pydantic import BaseModel
from datetime import datetime

class FileUpload(BaseModel):
    filename: str

class FileOut(BaseModel):
    id: int
    filename: str
    owner_id: int
    paired_user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
