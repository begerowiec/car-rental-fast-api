import datetime
from sqlalchemy import DECIMAL, Boolean, Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vehicle_type = Column(String, nullable=False)  # e.g., 'SUV', 'Sedan'
    registration_number = Column(String, unique=True, nullable=False)
    purchase_date = Column(Date, nullable=False)
    mileage = Column(Integer, default=0)
    status = Column(String, default='available')  # e.g., 'available', 'rented', 'maintenance'

    # Relationships
    orders = relationship('Order', back_populates='car')
    insurances = relationship('Insurance', back_populates='car')


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    identity_number = Column(String, unique=True, nullable=False)  # Passport or ID number
    pesel = Column(String, unique=True, nullable=False)  # National Identification Number
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
