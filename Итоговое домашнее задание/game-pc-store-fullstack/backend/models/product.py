from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.utils.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    rating = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))