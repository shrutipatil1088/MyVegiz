# app/services/product_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from fastapi import UploadFile

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import AppException
import cloudinary.uploader


MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def upload_product_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Product image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/products",
        resource_type="image"
    )
    return result["secure_url"]


# ---------- CREATE ----------
def create_product(
    db: Session,
    product: ProductCreate,
    product_image: UploadFile = None
):
    # Check category exists
    category = db.query(Category).filter(
        Category.id == product.category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    # Unique short name
    exists = db.query(Product).filter(
        Product.product_short_name == product.product_short_name,
        Product.is_delete == False
    ).first()

    if exists:
        raise AppException(status=400, message="Product short name already exists")

    image_url = upload_product_image(product_image) if product_image else None

    db_product = Product(
        category_id=product.category_id,
        product_name=product.product_name,
        product_short_name=product.product_short_name,
        product_image=image_url,
        is_active=product.is_active
    )

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while creating product")


# ---------- LIST ----------
def get_products(db: Session):
    return db.query(Product).filter(
        Product.is_delete == False
    ).order_by(Product.created_at.desc()).all()


# ---------- UPDATE ----------
def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
    product_image: UploadFile = None
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

    if product_data.category_id is not None:
        product.category_id = product_data.category_id

    if product_data.product_name is not None:
        product.product_name = product_data.product_name

    if product_data.product_short_name is not None:
        exists = db.query(Product).filter(
            Product.product_short_name == product_data.product_short_name,
            Product.id != product_id,
            Product.is_delete == False
        ).first()
        if exists:
            raise AppException(status=400, message="Product short name already exists")
        product.product_short_name = product_data.product_short_name

    if product_data.is_active is not None:
        product.is_active = product_data.is_active

    if product_image:
        product.product_image = upload_product_image(product_image)

    product.is_update = True

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating product")


# ---------- DELETE ----------
def soft_delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

    product.is_delete = True
    product.is_active = False
    product.deleted_at = func.now()

    db.commit()
    db.refresh(product)
    return product
