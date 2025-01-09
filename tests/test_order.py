import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ecommerce.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_order_success(client):
    # First, create a product
    response = client.post("/products/", json={
        "name": "Order Test Product",
        "description": "Product for order testing",
        "price": 20.0,
        "stock": 100
    })
    assert response.status_code == 201
    product = response.json()
    
    # Now, place an order
    response = client.post("/orders/", json={
        "products": [
            {"product_id": product["id"], "quantity": 2}
        ]
    })
    assert response.status_code == 201
    order = response.json()
    assert order["total_price"] == 40.0
    assert order["status"] == "completed"

def test_create_order_insufficient_stock(client):
    # Create a product with limited stock
    response = client.post("/products/", json={
        "name": "Limited Stock Product",
        "description": "Product with limited stock",
        "price": 15.0,
        "stock": 1
    })
    assert response.status_code == 201
    product = response.json()
    
    # Attempt to place an order exceeding stock
    response = client.post("/orders/", json={
        "products": [
            {"product_id": product["id"], "quantity": 5}
        ]
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock for product 'Limited Stock Product'"
