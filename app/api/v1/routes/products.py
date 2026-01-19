# app/api/v1/routes/products.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.schemas.response import APIResponse
from app.services.product_service import (
    create_product,
    get_products,
    update_product,
    soft_delete_product
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/create", response_model=APIResponse[ProductResponse])
def add_product(
    product: ProductCreate = Depends(ProductCreate.as_form),
    product_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    data = create_product(db, product, product_image)
    return {
        "status": 201,
        "message": "Product created successfully",
        "data": data
    }


@router.get("/list", response_model=APIResponse[List[ProductResponse]])
def list_products(db: Session = Depends(get_db),   
    current_user: User = Depends(get_current_user)
):
    data = get_products(db)
    return {
        "status": 200,
        "message": "Products fetched successfully",
        "data": data
    }



@router.put("/update", response_model=APIResponse[ProductResponse])
def update_product_api(
    product_id: int,
    product_image: UploadFile = File(None),  
    product: ProductUpdate = Depends(ProductUpdate.as_form),  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    updated_product = update_product(db, product_id, product, product_image)

    return {
        "status": 200,
        "message": "Product updated successfully",
        "data": updated_product
    }


@router.delete("/delete", response_model=APIResponse[ProductResponse])
def delete_product_api(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    data = soft_delete_product(db, product_id)
    return {
        "status": 200,
        "message": "Product deleted successfully",
        "data": data
    }
