

from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    category_id: int
    product_name: str
    product_short_name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    hsm_code: Optional[str] = None
    sku_code: Optional[str] = None
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        category_id: int = Form(...),
        product_name: str = Form(...),
        product_short_name: str = Form(...),
        short_description: Optional[str] = Form(None),
        long_description: Optional[str] = Form(None),
        hsm_code: Optional[str] = Form(None),
        sku_code: Optional[str] = Form(None),
        is_active: bool = Form(True),
    ):
        return cls(
            category_id=category_id,
            product_name=product_name,
            product_short_name=product_short_name,
            short_description=short_description,
            long_description=long_description,
            hsm_code=hsm_code,
            sku_code=sku_code,
            is_active=is_active
        )

    @field_validator("product_name", "product_short_name", mode="before")
    @classmethod
    def required_fields(cls, v, info):
        if v is None or not str(v).strip():
            raise ValueError(f"{info.field_name.replace('_',' ').title()} is required")
        return v.strip()


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_short_name: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    hsm_code: Optional[str] = None
    sku_code: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        product_name: Optional[str] = Form(None),
        product_short_name: Optional[str] = Form(None),
        short_description: Optional[str] = Form(None),
        long_description: Optional[str] = Form(None),
        hsm_code: Optional[str] = Form(None),
        sku_code: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            product_name=product_name.strip() if product_name else None,
            product_short_name=product_short_name.strip() if product_short_name else None,
            short_description=short_description.strip() if short_description else None,
            long_description=long_description.strip() if long_description else None,
            hsm_code=hsm_code.strip() if hsm_code else None,
            sku_code=sku_code.strip() if sku_code else None,
            is_active=is_active,
        )


class ProductImageResponse(BaseModel):
    product_image: str
    is_primary: bool

    class Config:
        orm_from_attributes = True


class ProductResponse(BaseModel):
    uu_id: str
    category_id: int
    product_name: str
    product_short_name: str
    slug: str
    short_description: Optional[str]
    long_description: Optional[str]
    hsm_code: Optional[str]
    sku_code: Optional[str]
    is_active: bool
    created_at: datetime
    images: List[ProductImageResponse]

    class Config:
        orm_from_attributes = True
