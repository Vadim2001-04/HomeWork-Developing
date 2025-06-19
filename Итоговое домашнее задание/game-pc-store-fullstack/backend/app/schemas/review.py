from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    user_id: int
    product_id: int
    text: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True