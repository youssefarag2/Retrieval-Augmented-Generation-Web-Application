# app/main.py
import logging
import sys

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
    )
logger = logging.getLogger(__name__)

# --- Imports ---
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .db import database, models
from .core.config import settings
# --- MODIFIED: Import the new notifications router ---
from .routers import auth, admin, query, notifications # Added notifications
from fastapi.middleware.cors import CORSMiddleware

# --- FastAPI Application Instance ---
app = FastAPI(
    title="RAG Application with Notifications",
    description="API for document RAG, user auth, query access control, and notifications.",
    version="0.6.0" # Bump version
)

# --- NEW: CORS Middleware Configuration ---
# Define the list of origins that are allowed to make cross-origin requests.
# Replace "http://localhost:5173" with the actual origin of your frontend application.
# You can use ["*"] to allow all origins, but this is less secure for production.
origins = [
    "http://localhost:5173", # Your frontend's origin
    # Add other origins if needed, e.g., your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True, # Allow cookies to be included in requests
    allow_methods=["*"],    # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allow all headers
)
# --- End of CORS Middleware Configuration ---

# --- Exception Handlers (Keep as is) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception for request {request.method} {request.url}: Status={exc.status_code}, Detail={exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception for request {request.method} {request.url}: {exc}")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "An internal server error occurred."})


# --- Application Event Handlers ---
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup sequence initiated...")
    try:
        logger.info("Attempting to create database tables...")
        database.Base.metadata.create_all(bind=database.engine) # This will create notifications & user_notification_status tables
        logger.info("Database tables check/creation completed.")
        logger.info("Initial admin user creation handled via /register endpoint.")

        if not settings.GOOGLE_API_KEY: logger.warning("GOOGLE_API_KEY not found.")
        else: logger.info("GOOGLE_API_KEY found.")
        
        from .services.file_processor import embedding_function, vector_store
        if embedding_function: logger.info("Embedding function initialized successfully.")
        else: logger.error("Embedding function FAILED to initialize.")
        if vector_store: logger.info("Vector store initialized successfully.")
        else: logger.error("Vector store FAILED to initialize.")
        
        try:
            from .services.rag_service import llm as rag_llm
            if rag_llm: logger.info("RAG service LLM initialized successfully.")
            else: logger.warning("RAG service LLM FAILED to initialize.")
        except ImportError: logger.error("Could not import LLM from RAG service.")
        except Exception as e_rag_llm: logger.error(f"Error checking RAG service LLM status: {e_rag_llm}")
        
        logger.info("Agent service components are expected to be running in a separate service (if applicable).")

    except Exception as e:
         logger.exception(f"CRITICAL ERROR during application startup: {e}")
    logger.info("Application startup sequence completed.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown sequence initiated...")
    logger.info("Application shutdown sequence completed.")


# --- Include API Routers ---
try:
    app.include_router(auth.router)
    app.include_router(admin.router)
    app.include_router(query.router)
    app.include_router(notifications.router) # <-- ADDED notifications router
    logger.info("API routers included successfully.")
except Exception as e:
     logger.exception(f"Failed to include API routers during setup: {e}")
     raise RuntimeError(f"Router setup failed: {e}")


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the RAG API with Notifications!"}

