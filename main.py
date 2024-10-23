from fastapi import FastAPI, Depends, HTTPException
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()

# Create all the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Car Endpoints
# ---------------------------

@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return cars


@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car
