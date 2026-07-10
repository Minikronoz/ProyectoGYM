from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from decimal import Decimal

from app.models.gym_equipment import UnitType


class GymEquipmentBase(BaseModel):
    gym_id: int
    exercise_id: int
    custom_alias: str
    unit_type: UnitType = UnitType.KG
    plate_weight_equivalent: Optional[Decimal] = None


class GymEquipmentCreate(GymEquipmentBase):
    created_by_user_id: Optional[int] = None


class GymEquipmentUpdate(BaseModel):
    custom_alias: Optional[str] = None
    unit_type: Optional[UnitType] = None
    plate_weight_equivalent: Optional[Decimal] = None


class GymEquipmentResponse(GymEquipmentBase):
    id: int
    created_by_user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class GymEquipmentWithDetails(GymEquipmentResponse):
    gym_name: Optional[str] = None
    exercise_name: Optional[str] = None
    target_muscle_group: Optional[str] = None
