from pydantic import BaseModel
from datetime import date, datetime


class CarBase(BaseModel):
    manufacturer: str
    model: str
    year: int
    vehicle_type: str
    registration_number: str
    purchase_date: date
    mileage: int
    status: str


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    identity_number: str
    pesel: str
    email: str
    phone_number: str


class OrderBase(BaseModel):
    client_id: int
    car_id: int
    start_date: datetime
    end_date: datetime
    status: str
    total_amount: float
    payment_status: str


class InsuranceBase(BaseModel):
    car_id: int
    policy_number: str
    company: str
    start_date: date
    end_date: date
