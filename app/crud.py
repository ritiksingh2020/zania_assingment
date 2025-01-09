from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
from .exceptions import InsufficientStockException

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    total_price = 0
    order_product_items = []
    
    for item in order.products:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        if product.stock < item.quantity:
            raise InsufficientStockException(f"Insufficient stock for product '{product.name}'")
        
        total_price += product.price * item.quantity
        product.stock -= item.quantity  # Deduct stock
        
        
        association = models.OrderProduct(
            product_id=product.id,
            quantity=item.quantity
        )
        order_product_items.append(association)
    
    
    db_order = models.Order(
        total_price=total_price,
        status=models.OrderStatus.completed,
        product_associations=order_product_items
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order
