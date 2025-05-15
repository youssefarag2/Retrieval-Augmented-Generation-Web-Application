# app/services/notification_service.py
import logging
from typing import List, Optional, Union
from datetime import datetime, timezone # <-- IMPORT timezone HERE

from sqlalchemy.orm import Session
# from sqlalchemy.sql import func # func is not used in the latest version of this file

from ..db import models, schemas # Import your DB models and Pydantic schemas
from ..core.config import settings # If needed for any settings

logger = logging.getLogger(__name__)

def create_notification(
    db: Session,
    message: str,
    target_level_input: Union[int, str], # Can be "all" or an int
    document_internal_id: Optional[str] = None,
    # created_by_user_id: Optional[int] = None # Optional: if tracking admin who sent it
) -> models.Notification:
    """
    Creates a new notification in the database.
    Converts 'all' for target_level_input to 0.
    """
    target_level_db = 0 # Default to "all students"
    if isinstance(target_level_input, str) and target_level_input.lower() == "all":
        target_level_db = 0
    elif isinstance(target_level_input, int) and 0 <= target_level_input <= 4: # 0 for all, 1-4 for specific
        target_level_db = target_level_input
    else:
        logger.error(f"Invalid target_level_input received in service: {target_level_input}. Defaulting to 'all'.")
        # Or raise ValueError("Invalid target level for notification.")

    db_notification = models.Notification(
        message=message,
        target_level=target_level_db,
        document_internal_id=document_internal_id,
        # created_by_user_id=created_by_user_id # If tracking creator
        # timestamp is handled by server_default=func.now() in the model
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    logger.info(f"Notification created: ID={db_notification.id}, TargetLevel={db_notification.target_level}, DocID={db_notification.document_internal_id}")
    return db_notification

def get_notifications_for_student(
    db: Session,
    user_id: int,
    student_level: int,
    fetch_seen: bool = False # Default to fetching only unseen
) -> List[schemas.NotificationDisplay]:
    """
    Fetches notifications relevant to a student, including their 'seen' status.
    - target_level 0 means for all students.
    - target_level matching student_level.
    - By default, only returns unseen notifications unless fetch_seen is True.
    """
    relevant_notifications_query = db.query(
        models.Notification,
        models.UserNotificationStatus.is_seen
    ).outerjoin(
        models.UserNotificationStatus,
        (models.Notification.id == models.UserNotificationStatus.notification_id) &
        (models.UserNotificationStatus.user_id == user_id)
    ).filter(
        (models.Notification.target_level == 0) | # For all students
        (models.Notification.target_level == student_level)
    ).order_by(models.Notification.timestamp.desc())

    if not fetch_seen:
        relevant_notifications_query = relevant_notifications_query.filter(
            (models.UserNotificationStatus.is_seen == False) |
            (models.UserNotificationStatus.is_seen == None)
        )
    
    results = relevant_notifications_query.all()

    notifications_display = []
    for notification, is_seen_status in results:
        notifications_display.append(
            schemas.NotificationDisplay(
                id=notification.id,
                message=notification.message,
                target_level=notification.target_level,
                document_internal_id=notification.document_internal_id,
                timestamp=notification.timestamp,
                is_seen=is_seen_status if is_seen_status is not None else False
            )
        )
    logger.info(f"Fetched {len(notifications_display)} notifications for student ID {user_id} (Level {student_level}), fetch_seen={fetch_seen}.")
    return notifications_display


def mark_notifications_as_seen(
    db: Session,
    user_id: int,
    notification_ids: List[int]
) -> bool:
    """
    Marks a list of notifications as seen for a specific user.
    Creates or updates UserNotificationStatus records.
    Returns True if successful, False otherwise.
    """
    if not notification_ids:
        return True 

    try:
        for notification_id in notification_ids:
            status_record = db.query(models.UserNotificationStatus).filter(
                models.UserNotificationStatus.user_id == user_id,
                models.UserNotificationStatus.notification_id == notification_id
            ).first()

            if status_record:
                if not status_record.is_seen:
                    status_record.is_seen = True
                    status_record.seen_at = datetime.now(timezone.utc) # timezone.utc is now defined
            else:
                new_status = models.UserNotificationStatus(
                    user_id=user_id,
                    notification_id=notification_id,
                    is_seen=True,
                    seen_at=datetime.now(timezone.utc) # timezone.utc is now defined
                )
                db.add(new_status)
        db.commit()
        logger.info(f"Marked {len(notification_ids)} notifications as seen for user ID {user_id}.")
        return True
    except Exception as e:
        db.rollback()
        logger.exception(f"Error marking notifications as seen for user ID {user_id}: {e}")
        return False
