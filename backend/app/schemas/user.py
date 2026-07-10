from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    google_id: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    google_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
