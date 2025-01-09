from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..exceptions import InsufficientStockException

router = APIRouter()

@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = crud.create_order(db=db, order=order)
        return db_order
    except InsufficientStockException as e:
        raise HTTPException(status_code=400, detail=str(e))
