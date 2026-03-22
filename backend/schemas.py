from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


# --- Equipment ---
class EquipmentBase(BaseModel):
    name: str
    status: str
    room: str
    problems: List[str] = Field(default_factory=list)


class EquipmentCreate(EquipmentBase):
    pass


class Equipment(EquipmentBase):
    id: int

    class Config:
        from_attributes = True  # заміна orm_mode


# --- Movement History ---
class MovementHistoryBase(BaseModel):
    equipment_id: int
    from_room: str
    to_room: str


class MovementHistory(MovementHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # заміна orm_mode


# --- Допоміжні схеми для PUT-запитів ---
class StatusUpdate(BaseModel):
    status: str


class MoveUpdate(BaseModel):
    to_room: str