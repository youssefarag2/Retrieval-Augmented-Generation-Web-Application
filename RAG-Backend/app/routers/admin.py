# app/routers/admin.py
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form, Body
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from typing import Optional, Dict, Union # Add Union
from pydantic import BaseModel, Field # <-- IMPORT BaseModel and Field HERE

from ..services import file_processor
from ..services import notification_service
from ..dependencies import get_current_admin_user, get_current_user_data
from ..db import schemas, database

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin_user)]
)
logger = logging.getLogger(__name__)

ALLOWED_ACCESS_TARGETS = [
    "public", "all_students",
    "level_1", "level_2", "level_3", "level_4",
    "admin_only"
]
ALLOWED_NOTIFICATION_TARGET_LEVELS = ["all", "0", "1", "2", "3", "4"]

# --- Document Upload Endpoint (Existing) ---
@router.post("/upload", response_model=schemas.UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    notification_message: Annotated[Optional[str], Form(description="Optional message for student notification.")] = None,
    notification_target_level: Annotated[Optional[str], Form(description=f"Target level for notification ('all', 0, 1, 2, 3, 4). Required if notification_message is provided.")] = None,
    doc_access_target: Annotated[str, Form(description=f"Access target for the document. Allowed values: {', '.join(ALLOWED_ACCESS_TARGETS)}")] = "admin_only",
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_admin_user: schemas.TokenData = Depends(get_current_user_data)
):
    filename = file.filename
    content_type = file.content_type
    logger.info(f"Admin '{current_admin_user.username}' initiating upload for file: {filename}, Access: {doc_access_target}")

    if doc_access_target not in ALLOWED_ACCESS_TARGETS:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid doc_access_target. Allowed: {ALLOWED_ACCESS_TARGETS}")

    notification_created_successfully = False
    parsed_target_level: Optional[int] = None

    if notification_message:
        if not notification_target_level:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="notification_target_level is required if notification_message is provided.")
        if notification_target_level not in ALLOWED_NOTIFICATION_TARGET_LEVELS:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid notification_target_level. Allowed: {', '.join(ALLOWED_NOTIFICATION_TARGET_LEVELS)}")
        try:
            if isinstance(notification_target_level, str) and notification_target_level.lower() == "all":
                parsed_target_level = 0
            else:
                parsed_target_level = int(notification_target_level)
            if not (0 <= parsed_target_level <= 4):
                raise ValueError("Parsed target level out of range 0-4.")
        except ValueError:
             raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid format for notification_target_level. Must be 'all' or an integer 0-4.")

    doc_id = None
    try:
        file_content = await file.read()
        if not file_content:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")
        
        doc_id = file_processor.process_and_embed_document(
            file_content, content_type, filename, doc_access_target
        )

        if not doc_id:
            logger.warning(f"File '{filename}' was not processed by file_processor.")
            return schemas.UploadResponse(
                message="File processing failed or returned no document ID.",
                filename=filename,
                doc_internal_id=None,
                error="File processing error.",
                notification_sent=False
            )

        if notification_message and parsed_target_level is not None: 
            try:
                notification_service.create_notification(
                    db=db,
                    message=notification_message,
                    target_level_input=parsed_target_level, 
                    document_internal_id=doc_id
                )
                notification_created_successfully = True
                logger.info(f"Notification created for document {doc_id} targeting level '{notification_target_level}'.")
            except Exception as e_notif:
                logger.error(f"Failed to create notification for document {doc_id}: {e_notif}")
        
        logger.info(f"File '{filename}' processed successfully. Internal ID: {doc_id}, Access: {doc_access_target}")
        return schemas.UploadResponse(
            message="File uploaded and processed successfully.",
            filename=filename,
            doc_internal_id=doc_id,
            notification_sent=notification_created_successfully
        )
    except RuntimeError as e_runtime: 
        logger.error(f"Configuration error during upload of '{filename}': {e_runtime}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e_runtime))
    except Exception as e_main:
        logger.exception(f"Unexpected error during upload of '{filename}': {e_main}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing '{filename}'."
        )
    finally:
        if file: 
            await file.close()

# --- NEW: General Broadcast Message Endpoint ---
class BroadcastMessageRequest(BaseModel): # BaseModel is now defined due to import
    message: str = Field(..., min_length=1, description="The message content to broadcast.")
    target_level: Union[int, str] = Field(..., description=f"Target student level ('all', 0, 1, 2, 3, 4). Allowed: {', '.join(ALLOWED_NOTIFICATION_TARGET_LEVELS)}")

@router.post("/broadcast", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str])
async def broadcast_message_to_students(
    request_body: BroadcastMessageRequest,
    db: Session = Depends(database.get_db),
    current_admin_user: schemas.TokenData = Depends(get_current_user_data) # For logging/audit
):
    """
    Allows an admin to send a general notification message to students.
    The message is not associated with any specific document upload.
    """
    logger.info(f"Admin '{current_admin_user.username}' initiating broadcast: Target='{request_body.target_level}', Message='{request_body.message[:50]}...'")

    # Validate and parse target_level
    parsed_target_level: int
    try:
        if isinstance(request_body.target_level, str) and request_body.target_level.lower() == "all":
            parsed_target_level = 0
        elif isinstance(request_body.target_level, str) and request_body.target_level.isdigit():
             parsed_target_level = int(request_body.target_level)
        elif isinstance(request_body.target_level, int):
            parsed_target_level = request_body.target_level
        else:
            raise ValueError("Invalid type for target_level")

        if not (0 <= parsed_target_level <= 4):
            raise ValueError("Target level out of range 0-4.")
            
    except ValueError:
         raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid notification_target_level: '{request_body.target_level}'. Allowed: {', '.join(ALLOWED_NOTIFICATION_TARGET_LEVELS)}"
        )

    try:
        notification_service.create_notification(
            db=db,
            message=request_body.message,
            target_level_input=parsed_target_level, # Use the parsed int value
            document_internal_id=None # No document associated with a general broadcast
            # created_by_user_id=current_admin_user.id # If tracking creator
        )
        logger.info(f"Broadcast message sent successfully by '{current_admin_user.username}' targeting level '{request_body.target_level}'.")
        return {"detail": "Broadcast message sent successfully."}
    except Exception as e:
        logger.exception(f"Failed to send broadcast message by '{current_admin_user.username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send broadcast message."
        )

