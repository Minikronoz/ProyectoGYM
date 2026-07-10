from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", response_model=List[ExerciseResponse])
def list_exercises(
    skip: int = 0,
    limit: int = 100,
    muscle_group: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Exercise)
    if muscle_group:
        query = query.filter(Exercise.target_muscle_group == muscle_group)
    return query.offset(skip).limit(limit).all()


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exercise = Exercise(**exercise_data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(exercise_id: int, exercise_data: ExerciseUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    for key, value in exercise_data.model_dump(exclude_unset=True).items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()
