from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.api.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse
from app.schemas.response import PaginatedAPIResponse

router = APIRouter()


@router.get("/list", response_model=PaginatedAPIResponse[List[CategoryResponse]])
def list_categories_web(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    # -------------------------------
    # Pagination calculation
    # -------------------------------
    offset = (page - 1) * limit

    # -------------------------------
    # Base query (WEB filters)
    # -------------------------------
    base_query = db.query(Category).filter(
        Category.is_delete == False,
        Category.is_active == True
    ).order_by(Category.created_at.desc())

    total_records = base_query.count()

    categories = base_query.offset(offset).limit(limit).all()

    total_pages = math.ceil(total_records / limit) if limit else 1

    pagination = {
        "total": total_records,
        "per_page": limit,
        "current_page": page,
        "total_pages": total_pages
    }

    return {
        "status": 200,
        "message": "Categories fetched successfully",
        "data": categories,
        "pagination": pagination
    }
