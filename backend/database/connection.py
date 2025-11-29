"""
Database Connection and Configuration
PostgreSQL database setup using async SQLAlchemy.
"""

import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# ------------------------------
# Load environment variables
# ------------------------------
DOTENV_PATH = "C:/app/backend/.env"
load_dotenv(dotenv_path=DOTENV_PATH)

# ------------------------------
# Database URL setup
# ------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres123@localhost/industrial_twin",
)

# Auto-convert sync URLs → async URLs
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

# print(f"USING DATABASE_URL: {DATABASE_URL}")

# ------------------------------
# Create async engine
# ------------------------------
engine = create_async_engine(DATABASE_URL,echo=False,future=True,pool_pre_ping=True,pool_size=10,
    max_overflow=20,
)

# ------------------------------
# Session maker
# ------------------------------
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ------------------------------
# Base class for ORM models
# ------------------------------
Base = declarative_base()

# ------------------------------
# Initialize database (creates tables)
# ------------------------------
async def init_db():
    """Initialize database: create all tables."""
    async with engine.begin() as conn:
        # Import models inside function to avoid circular imports
        from models import (
            alert,
            machine,
            maintenance_log,
            sensor_data,
            sop_task,
            spare_part,
            supplier,
            supply_chain_risk,
        )

        await conn.run_sync(Base.metadata.create_all)

    print("Database initialized successfully")

# ------------------------------
# Close database
# ------------------------------
async def close_db():
    """Close database connections."""
    await engine.dispose()
    print("Database connections closed")

# ------------------------------
# Dependency: get DB session
# ------------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide DB session for FastAPI."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
