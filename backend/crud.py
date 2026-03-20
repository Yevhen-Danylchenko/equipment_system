from sqlalchemy.orm import Session
from backend import models, schemas

def filter_equipment(db: Session, status: str | None = None, name: str | None = None):
    query = db.query(models.Equipment)
    if status:
        query = query.filter(models.Equipment.status == status)
    if name:
        query = query.filter(models.Equipment.name.ilike(f"%{name}%"))
    return query.all()

def create_equipment(db: Session, equipment: schemas.EquipmentCreate):
    db_equipment = models.Equipment(
        name=equipment.name,
        status=equipment.status,
        room=equipment.room,
        problems=equipment.problems or []
    )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

def get_equipment_list(db: Session):
    return db.query(models.Equipment).all()

def update_status(db: Session, equipment_id: int, status: str):
    eq = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if eq:
        eq.status = status
        db.commit()
        db.refresh(eq)
    return eq

def move_equipment(db: Session, equipment_id: int, to_room: str):
    eq = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if eq:
        from_room = eq.room
        eq.room = to_room
        db.commit()
        db.refresh(eq)
        history = models.MovementHistory(
            equipment_id=equipment_id,
            from_room=from_room,
            to_room=to_room
        )
        db.add(history)
        db.commit()
    return eq

def get_history(db: Session, equipment_id: int):
    return db.query(models.MovementHistory).filter(models.MovementHistory.equipment_id == equipment_id).all()