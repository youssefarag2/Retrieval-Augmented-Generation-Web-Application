# app/routers/auth.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..services import auth_service
from ..db import schemas, database, models
from ..core.config import settings
from ..dependencies import get_current_user_data

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
logger = logging.getLogger(__name__)

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: schemas.UserCreate, # Use the modified UserCreate schema
    db: Session = Depends(database.get_db)
):
    """
    Registers a new user.
    If role is 'student', 'level' (1-4) is required.
    If role is 'admin', 'level' must not be provided.
    """
    logger.info(f"Registration attempt for username: {user_data.username} with role: {user_data.role}, level: {user_data.level}")
    db_user = auth_service.get_user_by_username(db, username=user_data.username)
    if db_user:
        logger.warning(f"Registration failed: Username '{user_data.username}' already registered.")
        raise HTTPException(status_code=400, detail="Username already registered")

    # The role is taken directly from user_data.role.
    # The level is taken directly from user_data.level.
    # The UserCreate schema now handles validation for role and level.
    created_user = auth_service.create_user(db=db, user=user_data, role=user_data.role)
    return created_user


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(database.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add level to token data
    token_payload_data = {"sub": user.username, "role": user.role}
    if user.level is not None:
        token_payload_data["level"] = user.level

    access_token = auth_service.create_access_token(
        data=token_payload_data, expires_delta=access_token_expires
    )
    logger.info(f"Token generated for user: {user.username} (Role: {user.role}, Level: {user.level})")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.TokenData)
async def read_users_me(current_user_data: schemas.TokenData = Depends(get_current_user_data)):
    return current_user_data