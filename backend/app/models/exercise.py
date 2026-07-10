from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    technical_name = Column(String(100), nullable=False)
    target_muscle_group = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    gym_equipment = relationship("GymEquipment", back_populates="exercise")
