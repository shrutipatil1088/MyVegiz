from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi import Request

from app.api.dependencies import get_db
from app.schemas.category import CategoryCreate, CategoryResponse,CategoryUpdate
from app.schemas.response import APIResponse
from app.services.category_service import create_category, get_categories

from app.services.category_service import update_category
from app.services.category_service import soft_delete_category

from app.api.dependencies import get_current_user
from app.models.user import User
router = APIRouter()


@router.post("/create", response_model=APIResponse[CategoryResponse])
def add_category(
    category: CategoryCreate = Depends(CategoryCreate.as_form),
    category_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_category = create_category(db, category, category_image)

    return {
        "status": 201,
        "message": "Category created successfully",
        "data": new_category
    }


@router.get("/list", response_model=APIResponse[List[CategoryResponse]])
def list_categories(request: Request,
db: Session = Depends(get_db),current_user: User = Depends(get_current_user)
):

    if request.query_params:
        return {
            "status": 400,
            "message": "Query parameters are not allowed for this API",
            "data": []
        }


    categories = get_categories(db)

    if not categories:
        return {
            "status": 200,
            "message": "No categories found",
            "data": []
        }

    return {
        "status": 200,
        "message": "Categories fetched successfully",
        "data": categories
    }







@router.put("/update", response_model=APIResponse[CategoryResponse])
def update_category_api(
    uu_id: str,  # query param
    category: CategoryUpdate = Depends(CategoryUpdate.as_form),
    category_image: UploadFile = File(None),
    db: Session = Depends(get_db),    
    current_user: User = Depends(get_current_user)

):
    updated_category = update_category(
        db,
        uu_id,
        category,
        category_image
    )

    return {
        "status": 200,
        "message": "Category updated successfully",
        "data": updated_category
    }





@router.delete("/delete", response_model=APIResponse[CategoryResponse])
def delete_category_api(
    uu_id: str,   # query parameter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    deleted_category = soft_delete_category(db, uu_id)

    return {
        "status": 200,
        "message": "Category deleted successfully",
        "data": deleted_category
    }



