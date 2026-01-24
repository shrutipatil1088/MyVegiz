from sqlalchemy import Column, Integer, String, Boolean, DateTime,JSON
from sqlalchemy.sql import func
from app.db.base import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(255), nullable=False)
    city = Column(String(255), index=True, nullable=False)
    state = Column(String(255), index=True, nullable=False)
    # Polygon coordinates stored here
    polygon = Column(JSON, nullable=False)
    
    is_deliverable=Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
