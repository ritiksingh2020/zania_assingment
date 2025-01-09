from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import Base
import enum

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    
    
    order_associations = relationship("OrderProduct", back_populates="product")

class OrderStatus(enum.Enum):
    pending = "pending"
    completed = "completed"

class OrderProduct(Base):
    __tablename__ = 'order_product'
    
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    
    
    order = relationship("Order", back_populates="product_associations")
    product = relationship("Product", back_populates="order_associations")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    
    
    product_associations = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    
    
    @property
    def products(self):
        return [
            {
                "product": association.product,
                "quantity": association.quantity
            }
            for association in self.product_associations
        ]
