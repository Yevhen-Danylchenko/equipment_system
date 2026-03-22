# # backend/routers/equipment.py
# from fastapi import APIRouter, Depends
# from sqlalchemy import func
# from sqlalchemy.orm import Session
# from backend import database, schemas, crud, models
#
# router = APIRouter(prefix="/equipment", tags=["equipment"])
#
#
# @router.post("/", response_model=schemas.Equipment)
# def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(database.get_db)):
#     return crud.create_equipment(db, equipment)
#
#
# @router.get("/", response_model=list[schemas.Equipment])
# def get_equipment_list(db: Session = Depends(database.get_db)):
#     return crud.get_equipment_list(db)
#
#
# # # --- нові допоміжні схеми ---
# # class StatusUpdate(schemas.BaseModel):
# #     status: str
# #
# #
# # class MoveUpdate(schemas.BaseModel):
# #     to_room: str
# # # --------------------------------
#
#
# @router.put("/{equipment_id}/status", response_model=schemas.Equipment)
# def update_status(equipment_id: int, update: StatusUpdate, db: Session = Depends(database.get_db)):
#     return crud.update_status(db, equipment_id, update.status)
#
#
# @router.put("/{equipment_id}/move", response_model=schemas.Equipment)
# def move_equipment(equipment_id: int, update: MoveUpdate, db: Session = Depends(database.get_db)):
#     return crud.move_equipment(db, equipment_id, update.to_room)
#
#
# @router.get("/{equipment_id}/history", response_model=list[schemas.MovementHistory])
# def get_history(equipment_id: int, db: Session = Depends(database.get_db)):
#     return crud.get_history(db, equipment_id)
#
#
# @router.get("/filter", response_model=list[schemas.Equipment])
# def filter_equipment(status: str | None = None, name: str | None = None, db: Session = Depends(database.get_db)):
#     return crud.filter_equipment(db, status=status, name=name)
#
#
# @router.get("/broken", response_model=list[schemas.Equipment])
# def get_broken_equipment(db: Session = Depends(database.get_db)):
#     return crud.filter_equipment(db, status="несправне")
#
#
# @router.get("/stats")
# def get_stats(db: Session = Depends(database.get_db)):
#     total = db.query(models.Equipment).count()
#     broken = db.query(models.Equipment).filter(models.Equipment.status == "несправне").count()
#     by_room = db.query(models.Equipment.room, func.count(models.Equipment.id)).group_by(models.Equipment.room).all()
#     return {
#         "total": total,
#         "broken": broken,
#         "by_room": {room: count for room, count in by_room}
#     }

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend import database, schemas, crud, models

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.post("/", response_model=schemas.Equipment)
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(database.get_db)):
    return crud.create_equipment(db, equipment)


@router.get("/", response_model=list[schemas.Equipment])
def get_equipment_list(db: Session = Depends(database.get_db)):
    return crud.get_equipment_list(db)


@router.put("/{equipment_id}/status", response_model=schemas.Equipment)
def update_status(equipment_id: int, update: schemas.StatusUpdate, db: Session = Depends(database.get_db)):
    return crud.update_status(db, equipment_id, update.status)


@router.put("/{equipment_id}/move", response_model=schemas.Equipment)
def move_equipment(equipment_id: int, update: schemas.MoveUpdate, db: Session = Depends(database.get_db)):
    return crud.move_equipment(db, equipment_id, update.to_room)


@router.get("/{equipment_id}/history", response_model=list[schemas.MovementHistory])
def get_history(equipment_id: int, db: Session = Depends(database.get_db)):
    return crud.get_history(db, equipment_id)


@router.get("/filter", response_model=list[schemas.Equipment])
def filter_equipment(status: str | None = None, name: str | None = None, db: Session = Depends(database.get_db)):
    return crud.filter_equipment(db, status=status, name=name)


@router.get("/broken", response_model=list[schemas.Equipment])
def get_broken_equipment(db: Session = Depends(database.get_db)):
    return crud.filter_equipment(db, status="несправне")


@router.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    total = db.query(models.Equipment).count()
    broken = db.query(models.Equipment).filter(models.Equipment.status == "несправне").count()
    by_room = db.query(models.Equipment.room, func.count(models.Equipment.id)).group_by(models.Equipment.room).all()
    return {
        "total": total,
        "broken": broken,
        "by_room": {room: count for room, count in by_room}
    }