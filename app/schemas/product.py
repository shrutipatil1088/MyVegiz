# app/schemas/product.py
from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    category_id: int
    product_name: str
    product_short_name: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        category_id: int = Form(...),
        product_name: str = Form(...),
        product_short_name: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            category_id=category_id,
            product_name=product_name,
            product_short_name=product_short_name,
            is_active=is_active,
        )

    # ---------- REQUIRED ----------
    @field_validator("product_name", "product_short_name", mode="before")
    @classmethod
    def required_fields(cls, v, info):
        if v is None or not str(v).strip():
            raise ValueError(f"{info.field_name.replace('_',' ').title()} is required")
        return v.strip()



class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    product_name: Optional[str] = None
    product_short_name: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        category_id: Optional[int] = Form(None),
        product_name: Optional[str] = Form(None),
        product_short_name: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            category_id=category_id,
            product_name=product_name.strip() if product_name else None,
            product_short_name=product_short_name.strip() if product_short_name else None,
            is_active=is_active,
        )

    # ---------- VALIDATIONS ----------
    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError("Product name must be at least 3 characters long")
        return v

    @field_validator("product_short_name")
    @classmethod
    def validate_short_name(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError("Product short name must be at least 3 characters long")
        return v


class ProductResponse(BaseModel):
    id: int
    category_id: int
    product_name: str
    product_short_name: str
    product_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
