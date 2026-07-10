from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gyms.id"), nullable=False)
    date = Column(Date, nullable=False)
    general_notes = Column(Text, nullable=True)
    is_synced = Column(Boolean, default=False)
    client_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="workouts")
    gym = relationship("Gym", back_populates="workout_sessions")
    exercise_sets = relationship("ExerciseSet", back_populates="workout_session", cascade="all, delete-orphan")
