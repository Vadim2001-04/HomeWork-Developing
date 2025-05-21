from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models
from app.schemas import Product as ProductSchema
from app.utils.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.product.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product