from sqlalchemy.orm import Session
from sqlalchemy import func

from app.schemas.product_schemas import (
    ProductCreate,
    ProductResponse,
    UpdateProductPrice,
)
from fastapi import HTTPException
from app.db.models import Product, PriceHistory
from datetime import datetime, UTC

from app.services.scraper import price_scrape


def get_all_products(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(func.count(Product.id)).scalar()
    items = db.query(Product).offset(skip).limit(limit).all()

    return items, total


def create_new_product(db: Session, product: ProductCreate):
    try:
        db_product = Product(**product.model_dump())
        db_product.price_history.append(
            PriceHistory(price=db_product.target_price, created_at=datetime.now(UTC))
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    except Exception:
        db.rollback()
        raise


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter_by(id=product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="id not found")

    return product


def delete_product(db: Session, product_id: int):
    try:
        product = db.query(Product).filter_by(id=product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="id not found")

        db.delete(product)
        db.commit()

        return product

    except Exception:
        db.rollback()
        raise


def update_price(db: Session, price: UpdateProductPrice, product_id: int):
    try:
        product = db.query(Product).filter_by(id=product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="id not found")

        product.target_price = price.target_price

        history = PriceHistory(
            product_id=product.id,
            price=price.target_price,
            created_at=datetime.now(UTC),
        )

        db.add(history)

        db.commit()
        db.refresh(product)

        return product

    except Exception:
        db.rollback()
        raise


def get_product_history(db: Session, product_id: int):
    product = get_product(db, product_id)

    return product.price_history


def refresh_product_price(db: Session, product_id: int):
    product = get_product(db, product_id)

    price = price_scrape(product.url)
    if price is None:
        raise HTTPException(
            status_code=422, detail="Not available to scrape price from URL"
        )

    product.current_price = price
    db.add(
        PriceHistory(product_id=product_id, price=price, created_at=datetime.now(UTC))
    )
    db.commit()
    db.refresh(product)

    return product
