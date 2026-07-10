from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date
from decimal import Decimal

from app.database import get_db
from app.models.user import User
from app.models.gym_equipment import GymEquipment
from app.models.workout_session import WorkoutSession
from app.models.exercise_set import ExerciseSet
from app.schemas.analytics import ProgressResponse, ExerciseProgress, ProgressDataPoint
from app.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/progress", response_model=ProgressResponse)
def get_progress(
    gym_id: Optional[int] = None,
    exercise_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(GymEquipment).join(
        ExerciseSet, ExerciseSet.gym_equipment_id == GymEquipment.id
    ).join(
        WorkoutSession, WorkoutSession.id == ExerciseSet.workout_session_id
    ).filter(
        WorkoutSession.user_id == current_user.id
    )

    if gym_id:
        query = query.filter(GymEquipment.gym_id == gym_id)
    if exercise_id:
        query = query.filter(GymEquipment.exercise_id == exercise_id)

    equipment_list = query.all()

    progress_data = []
    for equipment in equipment_list:
        sets_query = db.query(ExerciseSet).join(
            WorkoutSession, WorkoutSession.id == ExerciseSet.workout_session_id
        ).filter(
            ExerciseSet.gym_equipment_id == equipment.id,
            WorkoutSession.user_id == current_user.id
        )

        if from_date:
            sets_query = sets_query.filter(WorkoutSession.date >= from_date)
        if to_date:
            sets_query = sets_query.filter(WorkoutSession.date <= to_date)

        sets = sets_query.all()

        volume_by_date = {}
        for s in sets:
            date_key = s.workout_session.date
            if date_key not in volume_by_date:
                volume_by_date[date_key] = {
                    "total_volume": Decimal("0"),
                    "max_weight": Decimal("0"),
                    "total_reps": 0,
                    "total_sets": 0
                }

            unit_type = equipment.unit_type.value if equipment.unit_type else "kg"

            if unit_type == "per_side_kg":
                weight = s.weight_value * 2
            elif unit_type == "plates" and equipment.plate_weight_equivalent:
                weight = s.weight_value * equipment.plate_weight_equivalent
            else:
                weight = s.weight_value

            volume_by_date[date_key]["total_volume"] += weight * s.reps_count
            if s.weight_value > volume_by_date[date_key]["max_weight"]:
                volume_by_date[date_key]["max_weight"] = s.weight_value
            volume_by_date[date_key]["total_reps"] += s.reps_count
            volume_by_date[date_key]["total_sets"] += 1

        data_points = [
            ProgressDataPoint(
                date=d,
                total_volume=v["total_volume"],
                max_weight=v["max_weight"],
                total_reps=v["total_reps"],
                total_sets=v["total_sets"]
            )
            for d, v in sorted(volume_by_date.items())
        ]

        progress_data.append(ExerciseProgress(
            exercise_id=equipment.exercise_id,
            exercise_name=equipment.exercise.technical_name if equipment.exercise else "Unknown",
            gym_equipment_id=equipment.id,
            equipment_alias=equipment.custom_alias,
            data_points=data_points
        ))

    return ProgressResponse(
        user_id=current_user.id,
        gym_id=gym_id,
        exercise_id=exercise_id,
        from_date=from_date,
        to_date=to_date,
        progress=progress_data
    )
