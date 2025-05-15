# app/core/config.py
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file first
load_dotenv()
logger = logging.getLogger(__name__)
logger.info(f"Loaded environment variables from: {os.path.abspath(os.getenv('DOTENV_PATH', '.env'))}")


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./rag_app.db"

    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-here" # CHANGE THIS!
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Google AI
    GOOGLE_API_KEY: str | None = None
    GEMINI_CHAT_MODEL: str = "gemini-1.5-flash" # Default if not in env

    # Embeddings
    EMBEDDING_MODEL_NAME: str = "jinaai/jina-embeddings-v3"

    # Vector Store
    CHROMA_DB_PATH: str = "./chroma_db"
    VECTOR_DB_COLLECTION_NAME: str = "rag_docs"

    class Config:
        # This makes Pydantic load from the .env file
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore' # Ignore extra fields in .env


settings = Settings()

# You can add validation here, e.g., check if GOOGLE_API_KEY is set
if not settings.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY is not set in the environment variables or .env file.")  