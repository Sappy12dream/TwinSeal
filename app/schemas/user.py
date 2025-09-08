# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Data received from client during signup
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# Data received from client during login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Data returned to client (excluding password)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
