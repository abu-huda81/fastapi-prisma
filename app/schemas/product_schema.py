from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    original_price: float
    new_price: Optional[float] = None
    expairy_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    pass

    class Config:
        from_attributes = True


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
