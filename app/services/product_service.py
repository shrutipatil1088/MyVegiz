# # app/services/product_service.py
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.sql import func
# from fastapi import UploadFile
# import uuid
# from slugify import slugify
# from app.models.product import Product
# from app.models.product_image import ProductImage

# from app.models.category import Category
# from app.schemas.product import ProductCreate, ProductUpdate
# from app.core.exceptions import AppException
# import cloudinary.uploader


# MAX_IMAGE_SIZE = 1 * 1024 * 1024
# ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


# def upload_product_image(file: UploadFile) -> str:
#     if file.content_type not in ALLOWED_TYPES:
#         raise AppException(status=400, message="Only JPG and PNG images are allowed")

#     contents = file.file.read()
#     if len(contents) > MAX_IMAGE_SIZE:
#         raise AppException(status=400, message="Product image must be less than 1 MB")

#     result = cloudinary.uploader.upload(
#         contents,
#         folder="myvegiz/products",
#         resource_type="image"
#     )
#     return result["secure_url"]


# # ---------- CREATE ----------
# def create_product(
#     db: Session,
#     product: ProductCreate,
#     product_image: UploadFile = None
# ):
#     # Check category exists
#     category = db.query(Category).filter(
#         Category.id == product.category_id,
#         Category.is_delete == False
#     ).first()

#     if not category:
#         raise AppException(status=404, message="Category not found")

#     # Unique short name
#     exists = db.query(Product).filter(
#         Product.product_short_name == product.product_short_name,
#         Product.is_delete == False
#     ).first()

#     if exists:
#         raise AppException(status=400, message="Product short name already exists")

#     image_url = upload_product_image(product_image) if product_image else None

#     db_product = Product(
#         category_id=product.category_id,
#         product_name=product.product_name,
#         product_short_name=product.product_short_name,
#         product_image=image_url,
#         is_active=product.is_active
#     )

#     try:
#         db.add(db_product)
#         db.commit()
#         db.refresh(db_product)
#         return db_product
#     except IntegrityError:
#         db.rollback()
#         raise AppException(status=500, message="Database error while creating product")


# # ---------- LIST ----------
# def get_products(db: Session):
#     return db.query(Product).filter(
#         Product.is_delete == False
#     ).order_by(Product.created_at.desc()).all()


# # ---------- UPDATE ----------
# def update_product(
#     db: Session,
#     product_id: int,
#     product_data: ProductUpdate,
#     product_image: UploadFile = None
# ):
#     product = db.query(Product).filter(
#         Product.id == product_id,
#         Product.is_delete == False
#     ).first()

#     if not product:
#         raise AppException(status=404, message="Product not found")

#     if product_data.category_id is not None:
#         product.category_id = product_data.category_id

#     if product_data.product_name is not None:
#         product.product_name = product_data.product_name

#     if product_data.product_short_name is not None:
#         exists = db.query(Product).filter(
#             Product.product_short_name == product_data.product_short_name,
#             Product.id != product_id,
#             Product.is_delete == False
#         ).first()
#         if exists:
#             raise AppException(status=400, message="Product short name already exists")
#         product.product_short_name = product_data.product_short_name

#     if product_data.is_active is not None:
#         product.is_active = product_data.is_active

#     if product_image:
#         product.product_image = upload_product_image(product_image)

#     product.is_update = True

#     try:
#         db.commit()
#         db.refresh(product)
#         return product
#     except IntegrityError:
#         db.rollback()
#         raise AppException(status=500, message="Database error while updating product")


# # ---------- DELETE ----------
# def soft_delete_product(db: Session, product_id: int):
#     product = db.query(Product).filter(
#         Product.id == product_id,
#         Product.is_delete == False
#     ).first()

#     if not product:
#         raise AppException(status=404, message="Product not found")

#     product.is_delete = True
#     product.is_active = False
#     product.deleted_at = func.now()

#     db.commit()
#     db.refresh(product)
#     return product




import uuid
import re
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile

from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import AppException
import cloudinary.uploader
from sqlalchemy.orm import joinedload


MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def upload_product_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    content = file.file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Product image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        content,
        folder="myvegiz/products",
        resource_type="image"
    )
    return result["secure_url"]


def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# ---------- CREATE ----------
def create_product(
    db: Session,
    product: ProductCreate,
    images: list[UploadFile]
):
    category = db.query(Category).filter(
        Category.id == product.category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    uu_id = str(uuid.uuid4())
    slug = generate_slug(product.product_name)

    if db.query(Product).filter(Product.slug == slug, Product.is_delete == False).first():
        raise AppException(status=400, message="Product already exists")

    db_product = Product(
        uu_id=uu_id,
        category_id=product.category_id,
        product_name=product.product_name,
        product_short_name=product.product_short_name,
        slug=slug,
        short_description=product.short_description,
        long_description=product.long_description,
        hsm_code=product.hsm_code,
        sku_code=product.sku_code,
        is_active=product.is_active
    )

    try:
        db.add(db_product)
        db.flush()

        for index, image in enumerate(images or []):
            db.add(ProductImage(
                product_id=db_product.id,
                product_image=upload_product_image(image),
                is_primary=index == 0
            ))

        db.commit()
        product_with_images = db.query(Product).options(
            joinedload(Product.images)
        ).filter(Product.id == db_product.id).first()

        return product_with_images
    except IntegrityError as e:
        db.rollback()
        print("DB ERROR 👉", e.orig)   # 👈 THIS LINE

        raise AppException(status=500, message="Database error while creating product")


# ---------- LIST ----------
def get_products(db: Session):
    return db.query(Product).options(
        joinedload(Product.images)
    ).filter(
        Product.is_delete == False
    ).order_by(Product.created_at.desc()).all()


# ---------- UPDATE ----------
def update_product(
    db: Session,
    uu_id: str,
    data: ProductUpdate,
    images: list[UploadFile]
):
    product = db.query(Product).filter(
        Product.uu_id == uu_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

    # 🔐 UPDATE ONLY PROVIDED FIELDS
    if data.product_name is not None:
        product.product_name = data.product_name

    if data.product_short_name is not None:
        product.product_short_name = data.product_short_name
        product.slug = generate_slug(data.product_short_name)

    if data.short_description is not None:
        product.short_description = data.short_description

    if data.long_description is not None:
        product.long_description = data.long_description

    if data.hsm_code is not None:
        product.hsm_code = data.hsm_code

    if data.sku_code is not None:
        product.sku_code = data.sku_code

    if data.is_active is not None:
        product.is_active = data.is_active

    product.is_update = True
    product.updated_at = func.now()

    # 🖼️ OPTIONAL IMAGE UPDATE
    if images:
        with db.no_autoflush:
            db.query(ProductImage).filter(
                ProductImage.product_id == product.id
            ).delete()

        for index, image in enumerate(images):
            image_url = upload_product_image(image)
            db.add(ProductImage(
                product_id=product.id,
                product_image=image_url,
                is_primary=(index == 0)
            ))

    db.commit()


    db.commit()
    return db.query(Product).options(
    joinedload(Product.images)
    ).filter(Product.id == product.id).first()


# ---------- DELETE ----------
def soft_delete_product(db: Session, uu_id: str):
    product = db.query(Product).filter(
        Product.uu_id == uu_id,
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

