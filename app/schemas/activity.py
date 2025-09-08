# app/schemas/activity.py
from pydantic import BaseModel
from datetime import datetime

class ActivityOut(BaseModel):
    id: int
    user_id: int
    action: str
    details: str | None
    created_at: datetime

    class Config:
        orm_mode = True
