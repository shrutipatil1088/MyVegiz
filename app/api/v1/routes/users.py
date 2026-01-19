from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import APIResponse
from app.services.user_service import create_user, get_users
from fastapi import Depends


from app.schemas.user import UserUpdate 
from app.services.user_service import update_user
from app.services.user_service import soft_delete_user


from app.api.dependencies import get_current_user
from app.models.user import User
router = APIRouter()


@router.post("/create",response_model=APIResponse[UserResponse])
def add_user(
    user: UserCreate = Depends(UserCreate.as_form),
    profile_image: UploadFile = File(None), 
    db: Session = Depends(get_db),    
    current_user: User = Depends(get_current_user)
):
    user = create_user(db, user, profile_image)
    return {
        "status": 201,
        "message": "User created successfully",
        "data": user
    }


@router.get("/list",response_model=APIResponse[List[UserResponse]])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = get_users(db)

    if not users:
        return {
            "status": 200,
            "message": "No users found",
            "data": []
        }

    return {
        "status": 200,
        "message": "Users fetched successfully",
        "data": users
    }



@router.put("/update", response_model=APIResponse[UserResponse])
def update_user_api(
    user_id: int,  # query parameter
    profile_image: UploadFile = File(None),
    user: UserUpdate = Depends(UserUpdate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    updated_user = update_user(db, user_id, user, profile_image)

    return {
        "status": 200,
        "message": "User updated successfully",
        "data": updated_user
    }



@router.delete("/delete", response_model=APIResponse[UserResponse])
def delete_user_api(
    user_id: int,  # query parameter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    deleted_user = soft_delete_user(db, user_id)

    return {
        "status": 200,
        "message": "User deleted successfully",
        "data": deleted_user
    }
