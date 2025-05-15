# app/services/auth_service.py
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.config import settings
from ..db import models, schemas
# SessionLocal might still be needed if you reinstate auto-admin creation or for other services
# from ..db.database import SessionLocal

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}", exc_info=True)
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, role: str) -> models.User: # Role is now more explicit
    hashed_password = get_password_hash(user.password)
    user_level = None
    if role == "student":
        user_level = user.level # Assumes validation happened in schema
    elif user.level is not None: # Role is admin, but level somehow passed validation (should not happen)
        logger.warning(f"Level {user.level} provided for non-student role {role} during user creation for {user.username}. Ignoring level.")
        user_level = None # Ensure level is None for non-students

    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=role,
        level=user_level # Store level
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User '{user.username}' created with role '{role}' and level '{user_level if user_level else 'N/A'}'.")
    return db_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    logger.info(f"Attempting authentication for user: {username}")
    db_user = get_user_by_username(db, username=username)

    if not db_user:
        logger.warning(f"Authentication failed: User '{username}' not found.")
        return None

    if not verify_password(password, db_user.hashed_password):
        logger.warning(f"Authentication failed: Invalid password for user '{username}'.")
        return None

    logger.info(f"User '{username}' authenticated successfully (Role: {db_user.role}, Level: {db_user.level}).")
    return db_user

def decode_access_token(token: str) -> Optional[schemas.TokenData]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        level: int | None = payload.get("level") # <-- Decode level from token

        if username is None or role is None: # Level can be None for admins
            logger.error("Token missing username ('sub') or role claim.")
            return None
        token_data = schemas.TokenData(username=username, role=role, level=level)
        return token_data
    except JWTError as e:
         logger.error(f"JWT Error during token decoding: {e}")
         return None

# Automatic admin creation is commented out as per previous changes.
# You can reinstate a similar logic or handle admin creation manually/via a special script.
# def create_initial_admin_user(): ...