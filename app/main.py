from fastapi import FastAPI
from app.database import engine, Base
from app.api import products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Platform API")

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
