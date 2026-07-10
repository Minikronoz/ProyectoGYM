from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.gym import Gym
from app.schemas.gym import GymCreate, GymResponse, GymUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/gyms", tags=["Gyms"])


@router.get("/", response_model=List[GymResponse])
def list_gyms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    gyms = db.query(Gym).offset(skip).limit(limit).all()
    return gyms


@router.get("/{gym_id}", response_model=GymResponse)
def get_gym(gym_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")
    return gym


@router.post("/", response_model=GymResponse, status_code=status.HTTP_201_CREATED)
def create_gym(gym_data: GymCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    gym = Gym(**gym_data.model_dump())
    db.add(gym)
    db.commit()
    db.refresh(gym)
    return gym


@router.put("/{gym_id}", response_model=GymResponse)
def update_gym(gym_id: int, gym_data: GymUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")

    for key, value in gym_data.model_dump(exclude_unset=True).items():
        setattr(gym, key, value)

    db.commit()
    db.refresh(gym)
    return gym


@router.delete("/{gym_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gym(gym_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")

    db.delete(gym)
    db.commit()
