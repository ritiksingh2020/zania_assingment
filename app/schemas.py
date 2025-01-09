from pydantic import BaseModel, Field
from typing import List, Optional
import enum


class OrderStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"


class ProductBase(BaseModel):
    name: str = Field(..., example="Laptop")
    description: Optional[str] = Field(None, example="A high-performance laptop.")
    price: float = Field(..., gt=0, example=999.99)
    stock: int = Field(..., ge=0, example=100)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderProductBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, example=2)


class OrderProductCreate(OrderProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class OrderProductDetail(BaseModel):
    product: ProductResponse
    quantity: int = Field(..., gt=0, example=2)

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    products: List[OrderProductBase]


class OrderCreate(OrderBase):
    pass


class Order(BaseModel):
    id: int = Field(..., alias="id", example=1)
    total_price: float = Field(..., gt=0, example=1999.98)
    status: OrderStatus = Field(..., example="completed")
    products: List[OrderProductDetail]

    class Config:
        orm_mode = True
