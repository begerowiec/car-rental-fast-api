import models
import schemas
from fastapi import FastAPI, Depends, HTTPException, Request, status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

# Import the ValidationErrorResponse model
from schemas import ValidationErrorResponse


app = FastAPI()

# Create all the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    title="Car Rental API",
    description="API Documentation for Car Rental Management System.",
    version="1.0.0",
    contact={
        "name": "Support",
        "email": "adrian@soft4you.com.pl",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Dependency to get a database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Custom exception handler for validation errors


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract errors from the exception
    errors = exc.errors()
    error_details = []

    for error in errors:
        loc = error['loc']
        if len(loc) > 1 and loc[0] == 'body':
            field_name = loc[1]
        else:
            field_name = " -> ".join([str(l) for l in loc])

        error_details.append({
            "field": field_name,
            "message": error['msg'],
            "type": error['type']
        })

    # Create a custom error response
    error_response = {
        "message": "Validation Error",
        "errors": error_details
    }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response
    )


# ---------------------------
# Car Endpoints
# ---------------------------

@app.post(
    "/cars/",
    response_model=schemas.Car,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Bad Request - Validation Error or Uniqueness Constraint Violation",
            "model": ValidationErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "Validation Error": {
                            "summary": "Validation Error Example",
                            "value": {
                                "message": "Validation Error",
                                "errors": [
                                    {
                                        "field": "manufacturer",
                                        "message": "field required",
                                        "type": "value_error.missing"
                                    }
                                ]
                            }
                        },
                        "Uniqueness Constraint Violation": {
                            "summary": "Uniqueness Constraint Violation Example",
                            "value": {
                                "errors": [
                                    {
                                        "detail": "Registration number already exists."
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    tags=["Cars"]
)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    # Check if the registration number already exists
    existing_car = db.query(models.Car).filter(
        models.Car.registration_number == car.registration_number).first()
    if existing_car:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration number already exists."
        )

    db_car = models.Car(**car.dict())
    try:
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    except IntegrityError as e:
        db.rollback()
        # Handle possible race condition or other integrity errors
        error_message = str(e.orig)
        if "UNIQUE constraint failed" in error_message and "cars.registration_number" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration number already exists."
            )
        else:
            # For other integrity errors, return a generic message
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database integrity error."
            )


@app.get("/cars/", tags=["Cars"], response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return cars


@app.get("/cars/{car_id}", tags=["Cars"], response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.put("/cars/{car_id}", tags=["Cars"], response_model=schemas.Car)
def update_car(car_id: int, car_update: schemas.CarUpdate, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    for key, value in car_update.dict(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car


@app.delete("/cars/{car_id}", tags=["Cars"], status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()

# ---------------------------
# Client Endpoints
# ---------------------------


@app.post("/clients/", tags=["Clients"], response_model=schemas.Client, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.get("/clients/", tags=["Clients"], response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    return clients


@app.get("/clients/{client_id}", tags=["Clients"], response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(
        models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.put("/clients/{client_id}", tags=["Clients"], response_model=schemas.Client)
def update_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(
        models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", tags=["Clients"])
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(
        models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"detail": "Client deleted"}

# ---------------------------
# Order Endpoints
# ---------------------------


@app.post("/orders/", tags=["Orders"], response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", tags=["Orders"], response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders


@app.get("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}


# ---------------------------
# Insurance Endpoints
# ---------------------------

@app.post("/insurances/", tags=["Insurances"], response_model=schemas.Insurance, status_code=status.HTTP_201_CREATED)
def create_insurance(insurance: schemas.InsuranceCreate, db: Session = Depends(get_db)):
    db_insurance = models.Insurance(**insurance.dict())
    db.add(db_insurance)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance


@app.get("/insurances/", tags=["Insurances"], response_model=List[schemas.Insurance])
def read_insurances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    insurances = db.query(models.Insurance).offset(skip).limit(limit).all()
    return insurances


@app.get("/insurances/{insurance_id}", tags=["Insurances"], response_model=schemas.Insurance)
def read_insurance(insurance_id: int, db: Session = Depends(get_db)):
    insurance = db.query(models.Insurance).filter(
        models.Insurance.id == insurance_id).first()
    if insurance is None:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance


@app.put("/insurances/{insurance_id}", tags=["Insurances"], response_model=schemas.Insurance)
def update_insurance(insurance_id: int, insurance_update: schemas.InsuranceUpdate, db: Session = Depends(get_db)):
    insurance = db.query(models.Insurance).filter(
        models.Insurance.id == insurance_id).first()
    if insurance is None:
        raise HTTPException(status_code=404, detail="Insurance not found")
    for key, value in insurance_update.dict(exclude_unset=True).items():
        setattr(insurance, key, value)
    db.commit()
    db.refresh(insurance)
    return insurance


@app.delete("/insurances/{insurance_id}", tags=["Insurances"])
def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    insurance = db.query(models.Insurance).filter(
        models.Insurance.id == insurance_id).first()
    if insurance is None:
        raise HTTPException(status_code=404, detail="Insurance not found")
    db.delete(insurance)
    db.commit()
    return {"detail": "Insurance deleted"}
