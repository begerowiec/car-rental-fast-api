from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

# ---------------------------
# Car Schemas
# ---------------------------


class CarBase(BaseModel):
    manufacturer: str = Field(...,
                              description="The car's manufacturer.", max_length=100)
    model: str = Field(..., description="The car model.", max_length=100)
    year: int = Field(..., description="The year the car was produced.")
    vehicle_type: str = Field(
        ..., description="Type of vehicle (e.g., 'SUV', 'Sedan').", max_length=50)
    registration_number: str = Field(
        ..., description="Unique registration number of the car.", max_length=50)
    purchase_date: date = Field(...,
                                description="Date when the car was purchased.")
    kilometers: int = Field(
        0, description="Current mileage of the car in kilometers.")
    status: str = Field(
        'available', description="Current status of the car (e.g., 'available', 'rented', 'maintenance').", max_length=50)


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    manufacturer: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    year: Optional[int]
    vehicle_type: Optional[str] = Field(None, max_length=50)
    registration_number: Optional[str] = Field(None, max_length=50)
    purchase_date: Optional[date]
    kilometers: Optional[int]
    status: Optional[str] = Field(None, max_length=50)


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

# ---------------------------
# Client Schemas
# ---------------------------


class ClientBase(BaseModel):
    first_name: str = Field(...,
                            description="Client's first name.", max_length=100)
    last_name: str = Field(...,
                           description="Client's last name.", max_length=100)
    date_of_birth: date = Field(..., description="Client's date of birth.")
    identity_number: str = Field(
        ..., description="Client's identity number (e.g., passport or ID card number).", max_length=50)
    pesel: str = Field(...,
                       description="Client's PESEL number.", max_length=20)
    email: str = Field(...,
                       description="Client's email address.", max_length=150)
    phone_number: str = Field(...,
                              description="Client's phone number.", max_length=20)


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date]
    identity_number: Optional[str] = Field(None, max_length=50)
    pesel: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=150)
    phone_number: Optional[str] = Field(None, max_length=20)


class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# Order Schemas
# ---------------------------


class OrderBase(BaseModel):
    client_id: int = Field(...,
                           description="ID of the client placing the order.")
    car_id: int = Field(..., description="ID of the car being rented.")
    start_date: datetime = Field(...,
                                 description="Start date and time of the rental.")
    end_date: datetime = Field(...,
                               description="End date and time of the rental.")
    status: str = Field(
        'pending', description="Current status of the order (e.g., 'pending', 'active', 'completed', 'canceled').", max_length=50)
    total_amount: float = Field(...,
                                description="Total amount for the rental.")
    payment_status: str = Field(
        'unpaid', description="Payment status of the order (e.g., 'paid', 'unpaid').", max_length=50)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    client_id: Optional[int]
    car_id: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[str] = Field(None, max_length=50)
    total_amount: Optional[float]
    payment_status: Optional[str] = Field(None, max_length=50)


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

# ---------------------------
# Insurance Schemas
# ---------------------------


class InsuranceBase(BaseModel):
    car_id: int = Field(..., description="ID of the car insured.")
    policy_number: str = Field(...,
                               description="Unique insurance policy number.", max_length=100)
    company: str = Field(...,
                         description="Name of the insurance company.", max_length=100)
    start_date: date = Field(...,
                             description="Start date of the insurance policy.")
    end_date: date = Field(...,
                           description="End date of the insurance policy.")


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    car_id: Optional[int]
    policy_number: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date]
    end_date: Optional[date]


class Insurance(InsuranceBase):
    id: int

    class Config:
        orm_mode = True
