from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    url: str
    target_price: Decimal


class UpdateProductPrice(BaseModel):
    target_price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    current_price: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    limit: int


class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
