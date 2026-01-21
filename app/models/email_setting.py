
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class EmailSetting(Base):
    __tablename__ = "email_settings"

    id = Column(Integer, primary_key=True)
    protocol = Column(String(50), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    encryption = Column(String(20), nullable=False)

    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)  # encrypted
    from_name = Column(String(255), nullable=False)
    from_email = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

