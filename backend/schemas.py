from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class EquipmentBase(BaseModel):
    name: str
    status: str
    room: str
    problems: Optional[List[str]] = []

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int
    class Config:
        orm_mode = True

class MovementHistoryBase(BaseModel):
    equipment_id: int
    from_room: str
    to_room: str

class MovementHistory(MovementHistoryBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True