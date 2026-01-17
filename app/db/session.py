from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# Create database engine & session
# Open DB → do work → close DB

# Creates a connection bridge between FastAPI and PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# creates DB sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,
    bind=engine
)

