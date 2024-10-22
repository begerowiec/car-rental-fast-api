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

    # Relationships
    orders = relationship('Order', back_populates='client')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default='pending')  # e.g., 'pending', 'active', 'completed', 'canceled'
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(String, default='unpaid')  # e.g., 'paid', 'unpaid'

    # Relationships
    client = relationship('Client', back_populates='orders')
    car = relationship('Car', back_populates='orders')

