from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    rating: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True