from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.user import User
from app.models.gym import Gym
from app.models.exercise import Exercise
from app.models.gym_equipment import GymEquipment
from app.models.workout_session import WorkoutSession
from app.models.exercise_set import ExerciseSet
from app.schemas.workout_session import WorkoutSessionCreate, WorkoutSessionResponse, WorkoutSessionUpdate, WorkoutSessionWithSets
from app.schemas.exercise_set import ExerciseSetCreate, ExerciseSetResponse, ExerciseSetWithEquipment
from app.schemas.gym_equipment import GymEquipmentCreate, GymEquipmentResponse, GymEquipmentWithDetails
from app.dependencies import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/sessions", response_model=List[WorkoutSessionResponse])
def list_sessions(
    skip: int = 0,
    limit: int = 50,
    gym_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(WorkoutSession).filter(WorkoutSession.user_id == current_user.id)
    if gym_id:
        query = query.filter(WorkoutSession.gym_id == gym_id)
    if from_date:
        query = query.filter(WorkoutSession.date >= from_date)
    if to_date:
        query = query.filter(WorkoutSession.date <= to_date)

    return query.order_by(WorkoutSession.date.desc()).offset(skip).limit(limit).all()


@router.get("/sessions/{session_id}", response_model=WorkoutSessionWithSets)
def get_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).options(
        joinedload(WorkoutSession.exercise_sets).joinedload(ExerciseSet.gym_equipment)
    ).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_data: WorkoutSessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    gym = db.query(Gym).filter(Gym.id == session_data.gym_id).first()
    if not gym:
        raise HTTPException(status_code=400, detail="Gym not found")

    session = WorkoutSession(
        user_id=current_user.id,
        gym_id=session_data.gym_id,
        date=session_data.date,
        general_notes=session_data.general_notes,
        client_id=session_data.client_id,
        is_synced=True
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.put("/sessions/{session_id}", response_model=WorkoutSessionResponse)
def update_session(session_id: int, session_data: WorkoutSessionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    for key, value in session_data.model_dump(exclude_unset=True).items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()


@router.post("/sets", response_model=ExerciseSetResponse, status_code=status.HTTP_201_CREATED)
def create_set(set_data: ExerciseSetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if set_data.workout_session_id:
        session = db.query(WorkoutSession).filter(
            WorkoutSession.id == set_data.workout_session_id,
            WorkoutSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(status_code=400, detail="Session not found or not owned by user")

    equipment = db.query(GymEquipment).filter(GymEquipment.id == set_data.gym_equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=400, detail="Equipment not found")

    exercise_set = ExerciseSet(**set_data.model_dump())
    db.add(exercise_set)
    db.commit()
    db.refresh(exercise_set)
    return exercise_set


@router.get("/equipment", response_model=List[GymEquipmentWithDetails])
def list_equipment(
    skip: int = 0,
    limit: int = 100,
    gym_id: Optional[int] = None,
    exercise_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(GymEquipment).options(
        joinedload(GymEquipment.gym),
        joinedload(GymEquipment.exercise)
    )

    if gym_id:
        query = query.filter(GymEquipment.gym_id == gym_id)
    if exercise_id:
        query = query.filter(GymEquipment.exercise_id == exercise_id)

    equipment_list = query.offset(skip).limit(limit).all()
    result = []
    for eq in equipment_list:
        result.append(GymEquipmentWithDetails(
            id=eq.id,
            gym_id=eq.gym_id,
            exercise_id=eq.exercise_id,
            custom_alias=eq.custom_alias,
            unit_type=eq.unit_type,
            plate_weight_equivalent=eq.plate_weight_equivalent,
            created_by_user_id=eq.created_by_user_id,
            created_at=eq.created_at,
            gym_name=eq.gym.name if eq.gym else None,
            exercise_name=eq.exercise.technical_name if eq.exercise else None,
            target_muscle_group=eq.exercise.target_muscle_group if eq.exercise else None
        ))
    return result


@router.post("/equipment", response_model=GymEquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment_data: GymEquipmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    gym = db.query(Gym).filter(Gym.id == equipment_data.gym_id).first()
    if not gym:
        raise HTTPException(status_code=400, detail="Gym not found")

    exercise = db.query(Exercise).filter(Exercise.id == equipment_data.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=400, detail="Exercise not found")

    equipment = GymEquipment(
        **equipment_data.model_dump(),
        created_by_user_id=current_user.id
    )
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.get("/equipment/{equipment_id}/last-set", response_model=Optional[ExerciseSetWithEquipment])
def get_last_set_for_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    equipment = db.query(GymEquipment).options(
        joinedload(GymEquipment.exercise)
    ).filter(GymEquipment.id == equipment_id).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    last_set = db.query(ExerciseSet).join(WorkoutSession).filter(
        ExerciseSet.gym_equipment_id == equipment_id,
        WorkoutSession.user_id == current_user.id
    ).order_by(ExerciseSet.created_at.desc()).first()

    if not last_set:
        return None

    return ExerciseSetWithEquipment(
        id=last_set.id,
        workout_session_id=last_set.workout_session_id,
        gym_equipment_id=last_set.gym_equipment_id,
        set_number=last_set.set_number,
        set_type=last_set.set_type,
        weight_value=last_set.weight_value,
        reps_count=last_set.reps_count,
        is_to_failure=last_set.is_to_failure,
        set_notes=last_set.set_notes,
        created_at=last_set.created_at,
        equipment_alias=equipment.custom_alias,
        exercise_name=equipment.exercise.technical_name if equipment.exercise else None,
        unit_type=str(equipment.unit_type.value) if equipment.unit_type else None
    )
