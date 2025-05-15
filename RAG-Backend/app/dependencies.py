# app/dependencies.py
import logging
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel # <-- ADDED THIS IMPORT

from .services import auth_service
from .db import schemas # Import TokenData

logger = logging.getLogger(__name__)

# Existing HTTPBearer scheme for required authentication
bearer_scheme = HTTPBearer(auto_error=True)

# NEW: HTTPBearer scheme for OPTIONAL authentication
optional_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_data(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> schemas.TokenData:
    """
    Dependency to get the current authenticated user's data (including role) from token.
    Raises HTTPException if token is invalid or missing.
    """
    if not token:
        logger.warning("get_current_user_data: No token provided.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = auth_service.decode_access_token(token.credentials)
    if token_data is None or token_data.username is None or token_data.role is None:
        logger.warning("get_current_user_data: Authentication failed: Could not validate credentials/role from token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials from token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"get_current_user_data: Authenticated user data from token: {token_data.username} (Role: {token_data.role}, Level: {token_data.level})")
    return token_data


async def get_current_admin_user(
    current_user_data: schemas.TokenData = Depends(get_current_user_data)
    ) -> schemas.TokenData:
    """
    Dependency to ensure the current user has the 'admin' role based on token data.
    """
    if current_user_data.role != "admin":
        logger.warning(f"get_current_admin_user: Admin access denied for user: {current_user_data.username} (Role: {current_user_data.role})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have admin privileges",
        )
    logger.info(f"get_current_admin_user: Admin access granted for user: {current_user_data.username}")
    return current_user_data

# --- NEW: Dependency for Query Context (Optional Auth) ---
class UserQueryContext(BaseModel): # BaseModel is now imported
    role: str # 'guest', 'student', 'admin'
    level: Optional[int] = None # Student's level if applicable
    username: Optional[str] = None # Logged-in username

async def get_user_query_context(
    token: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer_scheme)
) -> UserQueryContext:
    """
    Determines the user context for querying.
    - If a valid token is provided, identifies as 'admin' or 'student' (with level).
    - If no token or an invalid token is provided, identifies as 'guest'.
    """
    if token:
        token_data = auth_service.decode_access_token(token.credentials)
        if token_data and token_data.username and token_data.role:
            logger.info(f"get_user_query_context: User identified from token: {token_data.username}, Role: {token_data.role}, Level: {token_data.level}")
            return UserQueryContext(
                role=token_data.role,
                level=token_data.level,
                username=token_data.username
            )
        else:
            logger.info("get_user_query_context: Invalid token provided, treating as guest.")
            return UserQueryContext(role="guest")
    else:
        logger.info("get_user_query_context: No token provided, treating as guest.")
        return UserQueryContext(role="guest")

