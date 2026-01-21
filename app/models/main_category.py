from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class MainCategory(Base):
    __tablename__ = "main_categories"

    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)
    main_category_name = Column(String(255), nullable=False)
    slug = Column(String(255), index=True, nullable=False)
    main_category_image = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
