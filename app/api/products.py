from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.schemas.product_schemas import (
    ProductCreate,
    ProductResponse,
    UpdateProductPrice,
    PaginatedResponse,
    PriceHistoryResponse,
)
from app.services.product_service import (
    create_new_product,
    get_product,
    delete_product,
    update_price,
    get_all_products,
    get_product_history,
    refresh_product_price,
)

from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=PaginatedResponse)
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items, total = get_all_products(db, skip, limit)
    return {"items": items, "total": total, "page": skip // limit + 1, "limit": limit}


@router.post("/", response_model=ProductResponse)
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_new_product(db, product)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)


@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product_price(
    price: UpdateProductPrice, product_id: int, db: Session = Depends(get_db)
):
    return update_price(db, price, product_id)


@router.get("/{product_id}/history", response_model=list[PriceHistoryResponse])
async def get_product_price_history(product_id: int, db: Session = Depends(get_db)):
    return get_product_history(db, product_id)


@router.post("/{product_id}/refresh", response_model=ProductResponse)
async def refresh_price(product_id: int, db: Session = Depends(get_db)):
    return refresh_product_price(db, product_id)
