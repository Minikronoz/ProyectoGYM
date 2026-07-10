from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal


class ExerciseProgress(BaseModel):
    exercise_id: int
    exercise_name: str
    gym_equipment_id: int
    equipment_alias: str
    data_points: List["ProgressDataPoint"]


class ProgressDataPoint(BaseModel):
    date: date
    total_volume: Decimal
    max_weight: Decimal
    total_reps: int
    total_sets: int


class ProgressResponse(BaseModel):
    user_id: int
    gym_id: Optional[int] = None
    exercise_id: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    progress: List[ExerciseProgress]


from typing import List
ExerciseProgress.model_rebuild()
