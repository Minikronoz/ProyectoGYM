from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.models.exercise_set import SetType


class ExerciseSetBase(BaseModel):
    gym_equipment_id: int
    set_number: int
    set_type: SetType = SetType.NORMAL
    weight_value: Decimal
    reps_count: int
    is_to_failure: bool = False
    set_notes: Optional[str] = None


class ExerciseSetCreate(ExerciseSetBase):
    workout_session_id: Optional[int] = None


class ExerciseSetUpdate(BaseModel):
    set_number: Optional[int] = None
    set_type: Optional[SetType] = None
    weight_value: Optional[Decimal] = None
    reps_count: Optional[int] = None
    is_to_failure: Optional[bool] = None
    set_notes: Optional[str] = None


class ExerciseSetResponse(ExerciseSetBase):
    id: int
    workout_session_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExerciseSetWithEquipment(ExerciseSetResponse):
    equipment_alias: Optional[str] = None
    exercise_name: Optional[str] = None
    unit_type: Optional[str] = None
