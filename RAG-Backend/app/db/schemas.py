# app/db/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

# --- Auth Schemas ---
class Token(BaseModel):
    """Schema for the JWT access token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for data embedded within the JWT token."""
    username: str | None = None
    role: str | None = None
    level: Optional[int] = None # Student level, if applicable

class UserBase(BaseModel):
    """Base schema for user properties."""
    username: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    role: str = Field("student", description="User role ('student' or 'admin')")
    level: Optional[int] = Field(None, description="Student level (1-4), required if role is 'student'")

    @field_validator('role')
    @classmethod
    def validate_role(cls, value: str) -> str:
        """Validate that the role is either 'student' or 'admin'."""
        allowed_roles = {"student", "admin"}
        if value not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return value

    @field_validator('level')
    @classmethod
    def validate_level(cls, value: Optional[int], info) -> Optional[int]:
        """Validate student level: required for students, must be 1-4, and not allowed for admins."""
        # For Pydantic v2, context/other field values are in info.data
        role = info.data.get('role') if hasattr(info, 'data') else None
        
        if role == "student":
            if value is None:
                raise ValueError("Level is required for students.")
            if not 1 <= value <= 4:
                raise ValueError("Level must be between 1 and 4 for students.")
        elif value is not None: # Role is admin or other, but level is provided
            raise ValueError("Level should not be provided for non-student roles.")
        return value

class User(UserBase):
    """Schema for returning user information (excluding password)."""
    id: int
    role: str
    level: Optional[int] = None # Display level if it exists

    class Config:
        from_attributes = True # Pydantic v2 alias for orm_mode = True

# --- RAG Schemas ---
class SourceDocumentInfo(BaseModel):
    """Schema for information about a source document chunk."""
    filename: str
    page_number: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RagQueryRequest(BaseModel):
    """Schema for a RAG query request."""
    query: str

class RagQueryResponse(BaseModel):
    """Schema for a RAG query response."""
    answer: str
    sources: List[SourceDocumentInfo] = Field(default_factory=list)

# --- Admin Schemas ---
class UploadResponse(BaseModel):
    """Schema for the response after a successful file upload."""
    message: str
    filename: str
    doc_internal_id: Optional[str] = None
    error: Optional[str] = None
    notification_sent: Optional[bool] = Field(False, description="Indicates if a notification was processed for this upload")


# --- Notification Schemas ---
class NotificationBase(BaseModel):
    """Base schema for notification properties."""
    message: str
    # Using Union[int, str] to allow "all" as a string or 0 as int for flexibility in request,
    # but will be stored as int (0 for all, 1-4 for specific).
    target_level_input: Union[int, str] = Field(..., alias="targetLevel", description="Target student level (1-4, or 'all' for all students)")
    document_internal_id: Optional[str] = None # Link to a document if the notification is about it

class NotificationCreate(NotificationBase):
    """Schema for creating a new notification."""
    pass # Inherits all fields from NotificationBase

class NotificationDisplay(BaseModel):
    """Schema for displaying notifications to users."""
    id: int
    message: str
    target_level: int # As stored in the DB (0 for all, 1-4 for specific)
    document_internal_id: Optional[str] = None
    timestamp: datetime
    is_seen: bool = Field(False, description="Indicates if the current user has seen this notification")

    class Config:
        from_attributes = True

class MarkNotificationSeenRequest(BaseModel):
    """Schema for the request body when a user marks notification(s) as seen."""
    notification_ids: List[int] = Field(..., description="List of notification IDs to mark as seen")

