from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GymBase(BaseModel):
    name: str
    branch: Optional[str] = None
    address: Optional[str] = None


class GymCreate(GymBase):
    pass


class GymUpdate(BaseModel):
    name: Optional[str] = None
    branch: Optional[str] = None
    address: Optional[str] = None


class GymResponse(GymBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
