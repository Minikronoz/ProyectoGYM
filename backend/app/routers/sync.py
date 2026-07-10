from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.gym import Gym
from app.models.gym_equipment import GymEquipment
from app.models.workout_session import WorkoutSession
from app.models.exercise_set import ExerciseSet
from app.schemas.sync import SyncRequest, SyncResponse, SyncedSessionResponse, SyncSessionData
from app.dependencies import get_current_user

router = APIRouter(prefix="/sync", tags=["Sync"])


@router.post("/", response_model=SyncResponse)
def sync_workouts(sync_data: SyncRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    synced_sessions = []
    total_sets = 0

    for session_data in sync_data.sessions:
        existing_session = db.query(WorkoutSession).filter(
            WorkoutSession.client_id == session_data.client_session_id,
            WorkoutSession.user_id == current_user.id
        ).first()

        if existing_session:
            existing_session.general_notes = session_data.general_notes
            db.commit()
            session_id = existing_session.id
            session_status = "updated"
        else:
            new_session = WorkoutSession(
                user_id=current_user.id,
                gym_id=session_data.gym_id,
                date=session_data.date,
                general_notes=session_data.general_notes,
                client_id=session_data.client_session_id,
                is_synced=True
            )
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            session_id = new_session.id
            session_status = "created"

        synced_set_count = 0
        for set_data in session_data.sets:
            existing_set = db.query(ExerciseSet).filter(
                ExerciseSet.workout_session_id == session_id,
                ExerciseSet.gym_equipment_id == set_data.gym_equipment_id,
                ExerciseSet.set_number == set_data.set_number
            ).first()

            if not existing_set:
                new_set = ExerciseSet(
                    workout_session_id=session_id,
                    gym_equipment_id=set_data.gym_equipment_id,
                    set_number=set_data.set_number,
                    set_type=set_data.set_type,
                    weight_value=set_data.weight_value,
                    reps_count=set_data.reps_count,
                    is_to_failure=set_data.is_to_failure,
                    set_notes=set_data.set_notes
                )
                db.add(new_set)
                synced_set_count += 1

        db.commit()
        total_sets += synced_set_count

        synced_sessions.append(SyncedSessionResponse(
            client_session_id=session_data.client_session_id,
            server_session_id=session_id,
            synced_sets=synced_set_count,
            status=session_status
        ))

    return SyncResponse(
        synced_sessions=synced_sessions,
        total_sets_synced=total_sets,
        sync_timestamp=datetime.utcnow().isoformat()
    )
