from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.api.dependencies import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse
from app.schemas.response import PaginatedAPIResponse

router = APIRouter()


@router.get(
    "/list",
    response_model=PaginatedAPIResponse[List[ProductResponse]]
)
def list_products_web(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    category_id: Optional[int] = Query(None),
    sub_category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    query = db.query(Product).filter(
        Product.is_delete == False,
        Product.is_active == True
    )

    # 🔍 Optional filters
    if category_id:
        query = query.filter(Product.category_id == category_id)

    if sub_category_id:
        query = query.filter(Product.sub_category_id == sub_category_id)

    total_records = query.count()

    products = (
        query
        .order_by(Product.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = math.ceil(total_records / limit) if limit else 1

    return {
        "status": 200,
        "message": "Products fetched successfully",
        "data": products,
        "pagination": {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages
        }
    }
