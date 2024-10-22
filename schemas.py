from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# ---------------------------
# Car Schemas
# ---------------------------


class CarBase(BaseModel):
    manufacturer: str
    model: str
    year: int
    vehicle_type: str
    registration_number: str
    purchase_date: date
    kilometers: int
    status: str


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    manufacturer: Optional[str]
    model: Optional[str]
    year: Optional[int]
    vehicle_type: Optional[str]
    registration_number: Optional[str]
    purchase_date: Optional[date]
    kilometers: Optional[int]
    status: Optional[str]


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------
# Client Schemas
# ---------------------------

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    identity_number: str
    pesel: str
    email: str
    phone_number: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    identity_number: Optional[str]
    pesel: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]


class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# Order Schemas
# ---------------------------


class OrderBase(BaseModel):
    client_id: int
    car_id: int
    start_date: datetime
    end_date: datetime
    status: str
    total_amount: float
    payment_status: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    client_id: Optional[int]
    car_id: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[str]
    total_amount: Optional[float]
    payment_status: Optional[str]


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

# ---------------------------
# Insurance Schemas
# ---------------------------


class InsuranceBase(BaseModel):
    car_id: int
    policy_number: str
    company: str
    start_date: date
    end_date: date


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    car_id: Optional[int]
    policy_number: Optional[str]
    company: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class Insurance(InsuranceBase):
    id: int

    class Config:
        orm_mode = True
