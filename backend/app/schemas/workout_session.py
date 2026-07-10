from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class WorkoutSessionBase(BaseModel):
    gym_id: int
    date: date
    general_notes: Optional[str] = None


class WorkoutSessionCreate(WorkoutSessionBase):
    client_id: Optional[str] = None


class WorkoutSessionUpdate(BaseModel):
    general_notes: Optional[str] = None


class WorkoutSessionResponse(WorkoutSessionBase):
    id: int
    user_id: int
    is_synced: bool
    client_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkoutSessionWithSets(WorkoutSessionResponse):
    sets: List["ExerciseSetResponse"] = []


from app.schemas.exercise_set import ExerciseSetResponse
WorkoutSessionWithSets.model_rebuild()
