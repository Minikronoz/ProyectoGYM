from pydantic import BaseModel
from typing import Optional


class ExerciseBase(BaseModel):
    technical_name: str
    target_muscle_group: str
    description: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    technical_name: Optional[str] = None
    target_muscle_group: Optional[str] = None
    description: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        from_attributes = True
