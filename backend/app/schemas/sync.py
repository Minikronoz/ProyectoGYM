from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal

from app.models.exercise_set import SetType


class SyncSetData(BaseModel):
    client_set_id: str
    gym_equipment_id: int
    set_number: int
    set_type: SetType = SetType.NORMAL
    weight_value: Decimal
    reps_count: int
    is_to_failure: bool = False
    set_notes: Optional[str] = None


class SyncSessionData(BaseModel):
    client_session_id: str
    gym_id: int
    date: date
    general_notes: Optional[str] = None
    sets: List[SyncSetData]


class SyncRequest(BaseModel):
    sessions: List[SyncSessionData]
    client_created_at: Optional[str] = None


class SyncedSessionResponse(BaseModel):
    client_session_id: str
    server_session_id: int
    synced_sets: int
    status: str = "synced"


class SyncResponse(BaseModel):
    synced_sessions: List[SyncedSessionResponse]
    total_sets_synced: int
    sync_timestamp: str
