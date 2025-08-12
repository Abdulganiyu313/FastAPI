from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(Text)
    full_name = Column(String)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class Order(Base):
    
    ORDER_STATUS_CHOICES = (
        ("NEW", "New"),
        ("PENDING", "Pending"),
        ("IN-TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
    )
    
    PIZZA_SIZE_CHOICES = (
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large"),
        ("EXTRA_LARGE", "Extra Large"),
    )
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    order_status = Column(ChoiceType(choices=ORDER_STATUS_CHOICES), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZE_CHOICES), default="SMALL")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, quantity={self.quantity}, order_status={self.order_status}, pizza_size={self.pizza_size})>"