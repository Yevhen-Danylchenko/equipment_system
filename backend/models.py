from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="справне")
    room = Column(String)
    problems = Column(JSON, default=list)  # зберігаємо як JSON-рядок

    movements = relationship("MovementHistory", back_populates="equipment")

class MovementHistory(Base):
    __tablename__ = "movement_history"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    from_room = Column(String)
    to_room = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    equipment = relationship("Equipment", back_populates="movements")