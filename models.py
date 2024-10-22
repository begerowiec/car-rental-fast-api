from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    vehicle_type = Column(String(50), nullable=False)  # e.g., 'SUV', 'Sedan'
    registration_number = Column(String(50), unique=True, nullable=False)
    purchase_date = Column(Date, nullable=False)
    mileage = Column(Integer, default=0)
    # e.g., 'available', 'rented', 'maintenance'
    status = Column(String(50), default='available')

    # Relationships
    orders = relationship('Order', back_populates='car')
    insurances = relationship('Insurance', back_populates='car')


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    identity_number = Column(String(50), unique=True, nullable=False)
    pesel = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
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
    # e.g., 'pending', 'active', 'completed', 'canceled'
    status = Column(String(50), default='pending')
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    # e.g., 'paid', 'unpaid'
    payment_status = Column(String(50), default='unpaid')

    # Relationships
    client = relationship('Client', back_populates='orders')
    car = relationship('Car', back_populates='orders')


class Insurance(Base):
    __tablename__ = 'insurance'

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)
    policy_number = Column(String(100), unique=True, nullable=False)
    company = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Relationships
    car = relationship('Car', back_populates='insurances')
