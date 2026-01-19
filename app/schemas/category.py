from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime
import re


class CategoryCreate(BaseModel):
    category_name: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        category_name: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            category_name=category_name,
            is_active=is_active,
        )

    # ---------- REQUIRED ----------
    @field_validator("category_name", mode="before")
    @classmethod
    def required_category_name(cls, v):
        if v is None or not v.strip():
            raise ValueError("Category name is required")
        return v.strip()

    # ---------- FORMAT ----------
    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, v):
        if len(v) < 3:
            raise ValueError("Category name must be at least 3 characters long")
        return v


class CategoryResponse(BaseModel):
    id: int
    uu_id: str
    category_name: str
    slug: str
    category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True



class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        category_name: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            category_name=category_name.strip() if category_name else None,
            is_active=is_active,
        )

    # ---------- VALIDATION ----------
    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Category name is required")
            if len(v) < 3:
                raise ValueError("Category name must be at least 3 characters long")
        return v
