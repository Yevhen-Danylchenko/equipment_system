# backend/main.py
from fastapi import FastAPI
from backend import models, database
from backend.routers import equipment
from backend.models import Equipment, MovementHistory


# створюємо таблиці при старті
models.Base.metadata.create_all(bind=database.engine)

# створюємо FastAPI застосунок
app = FastAPI(title="Equipment Management System")

# підключаємо маршрути для роботи з обладнанням
app.include_router(equipment.router)

# тестовий кореневий маршрут
@app.get("/")
def root():
    return {"message": "Equipment API is running"}