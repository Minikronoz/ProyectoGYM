from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Gym(Base):
    __tablename__ = "gyms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    branch = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    equipment = relationship("GymEquipment", back_populates="gym")
    workout_sessions = relationship("WorkoutSession", back_populates="gym")
