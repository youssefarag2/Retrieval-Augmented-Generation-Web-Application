# app/routers/notifications.py
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..db import database, schemas, models # Import necessary items
from ..services import notification_service # Import your notification service
from ..dependencies import get_current_user_data # For authenticated user context

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(get_current_user_data)] # All notification endpoints require login
)
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[schemas.NotificationDisplay])
async def get_my_notifications(
    fetch_all: Optional[bool] = Query(False, description="Set to true to fetch all notifications including seen ones, otherwise only unseen are returned."),
    current_user: schemas.TokenData = Depends(get_current_user_data),
    db: Session = Depends(database.get_db)
):
    """
    Fetches notifications for the currently logged-in student.
    By default, only fetches unseen notifications.
    Admins can also use this to see what a student would see if they had a level (though admins typically don't have levels).
    """
    if current_user.role != "student" or current_user.level is None:
        # For now, only students with levels can have targeted notifications.
        # Admins could potentially see all, or this endpoint could be restricted.
        # Let's return an empty list for non-students or students without a level for now.
        # Or, you could allow admins to query for a specific level if desired.
        logger.info(f"User '{current_user.username}' (Role: {current_user.role}) attempted to fetch notifications. Endpoint primarily for students with levels.")
        if current_user.role == "admin": # Admins can see all notifications by target_level 0 (all students)
             # This logic could be expanded if admins need to see notifications for specific levels
            user_db = db.query(models.User).filter(models.User.username == current_user.username).first()
            if not user_db:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found in DB.")
            # Admins will see notifications targeted to "all" (level 0)
            # and we can simulate them having "is_seen" status for those
            return notification_service.get_notifications_for_student(
                db=db, user_id=user_db.id, student_level=0, fetch_seen=fetch_all # student_level 0 for "all"
            )
        return []

    # Fetch the full user object to get their ID
    user_db = db.query(models.User).filter(models.User.username == current_user.username).first()
    if not user_db:
        # This should ideally not happen if token is valid
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student user not found in database.")

    notifications = notification_service.get_notifications_for_student(
        db=db,
        user_id=user_db.id,
        student_level=current_user.level,
        fetch_seen=fetch_all
    )
    return notifications

@router.post("/mark-as-seen", status_code=status.HTTP_204_NO_CONTENT)
async def mark_notifications_seen(
    request: schemas.MarkNotificationSeenRequest,
    current_user: schemas.TokenData = Depends(get_current_user_data),
    db: Session = Depends(database.get_db)
):
    """
    Marks a list of specified notification IDs as seen for the currently logged-in user.
    """
    # Fetch the full user object to get their ID
    user_db = db.query(models.User).filter(models.User.username == current_user.username).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database.")

    if not request.notification_ids:
        # No IDs provided, nothing to do, but not an error.
        return

    success = notification_service.mark_notifications_as_seen(
        db=db,
        user_id=user_db.id,
        notification_ids=request.notification_ids
    )

    if not success:
        # This could happen if there's a DB error during the update.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notifications as seen."
        )
    # Return 204 No Content on success
    return

