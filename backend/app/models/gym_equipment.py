from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class UnitType(str, enum.Enum):
    KG = "kg"
    LBS = "lbs"
    PLATES = "plates"
    BODYWEIGHT = "bodyweight"
    PER_SIDE_KG = "per_side_kg"


class GymEquipment(Base):
    __tablename__ = "gym_equipment"

    id = Column(Integer, primary_key=True, index=True)
    gym_id = Column(Integer, ForeignKey("gyms.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    custom_alias = Column(String(150), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False, default=UnitType.KG)
    plate_weight_equivalent = Column(Numeric(5, 2), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    gym = relationship("Gym", back_populates="equipment")
    exercise = relationship("Exercise", back_populates="gym_equipment")
    created_by_user = relationship("User", back_populates="gym_equipment")
    exercise_sets = relationship("ExerciseSet", back_populates="gym_equipment")
