# app/db/database.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

logger = logging.getLogger(__name__)

try:
    engine = create_engine(
        settings.DATABASE_URL,
        # For SQLite, connect_args is needed to support multithreading (FastAPI runs in threads)
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    logger.info(f"Database engine created for URL: {settings.DATABASE_URL}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database session maker configured.")

    Base = declarative_base()
    logger.info("SQLAlchemy Base declarative base created.")

except Exception as e:
    logger.exception(f"Failed to initialize database components: {e}")
    # Depending on your app's needs, you might want to exit here or handle it differently
    raise RuntimeError(f"Database initialization failed: {e}")


def get_db():
    """Dependency function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """Creates database tables if they don't exist."""
    logger.info("Attempting to create database tables if they don't exist...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables checked/created successfully.")
    except Exception as e:
        logger.exception(f"Failed to create database tables: {e}")
        raise # Re-raise the exception to be caught during startup