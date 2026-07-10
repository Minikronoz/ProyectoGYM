from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class SetType(str, enum.Enum):
    WARMUP = "warmup"
    NORMAL = "normal"
    FAILURE = "failure"
    DROP_SET = "drop_set"


class ExerciseSet(Base):
    __tablename__ = "exercise_sets"

    id = Column(Integer, primary_key=True, index=True)
    workout_session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    gym_equipment_id = Column(Integer, ForeignKey("gym_equipment.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    set_type = Column(Enum(SetType), nullable=False, default=SetType.NORMAL)
    weight_value = Column(Numeric(6, 2), nullable=False)
    reps_count = Column(Integer, nullable=False)
    is_to_failure = Column(Boolean, default=False)
    set_notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True))

    workout_session = relationship("WorkoutSession", back_populates="exercise_sets")
    gym_equipment = relationship("GymEquipment", back_populates="exercise_sets")
