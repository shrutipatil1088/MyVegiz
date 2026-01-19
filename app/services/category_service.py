from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
from sqlalchemy.sql import func
import uuid
import re

from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.core.exceptions import AppException
import cloudinary.uploader


from app.schemas.category import CategoryUpdate


MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def upload_category_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    contents = file.file.read()

    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Category image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/categories",
        resource_type="image"
    )

    return result["secure_url"]


def generate_slug(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return slug


# ---------- CREATE CATEGORY ----------
def create_category(
    db: Session,
    category: CategoryCreate,
    category_image: UploadFile = None
):
    if not category_image:
        raise AppException(status=400, message="Category image is required")



    # Generate UUID & Slug
    uu_id = str(uuid.uuid4())
    slug = generate_slug(category.category_name)

    # Check slug uniqueness
    slug_exists = db.query(Category).filter(
        Category.slug == slug,
        Category.is_delete == False
    ).first()

    if slug_exists:
        raise AppException(status=400, message="Category already exists")

    image_url = None
    if category_image:
        image_url = upload_category_image(category_image)

    db_category = Category(
        uu_id=uu_id,
        category_name=category.category_name,
        slug=slug,
        category_image=image_url,
        is_active=category.is_active
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while creating category")


# ---------- LIST CATEGORIES ----------
def get_categories(db: Session):
    return db.query(Category).filter(
        Category.is_delete == False
    ).order_by(Category.created_at.desc()).all()






def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")

def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate,
    category_image: UploadFile = None
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    # ---------- NAME + SLUG ----------
    if category_data.category_name is not None:
        new_slug = generate_slug(category_data.category_name)

        slug_exists = db.query(Category).filter(
            Category.slug == new_slug,
            Category.is_delete == False,
            Category.id != category_id
        ).first()

        if slug_exists:
            raise AppException(status=400, message="Category already exists")

        category.category_name = category_data.category_name
        category.slug = new_slug

    # ---------- ACTIVE ----------
    if category_data.is_active is not None:
        category.is_active = category_data.is_active

    # ---------- IMAGE ----------
    if category_image:
        category.category_image = upload_category_image(category_image)

    category.is_update = True
    category.updated_at = func.now()

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating category")









def soft_delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    category.is_delete = True
    category.is_active = False
    category.deleted_at = func.now()

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while deleting category")
