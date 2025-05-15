# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # For default timestamp

from .database import Base # Assuming your SQLAlchemy Base is defined in database.py

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False) # 'admin' or 'student'
    level = Column(Integer, nullable=True) # e.g., 1, 2, 3, 4 for students

    # Relationship to the association table for seen notifications
    seen_notifications_assoc = relationship("UserNotificationStatus", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}', level='{self.level}')>"


# Notification Model
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    # Target level: 0 for all student levels, 1-4 for specific levels.
    target_level = Column(Integer, nullable=False, comment="0=all students, 1-4=specific level")
    # document_internal_id can be used to link to a specific document if the notification is about it
    document_internal_id = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to the association table
    seen_by_users_assoc = relationship("UserNotificationStatus", back_populates="notification")

    def __repr__(self):
        return f"<Notification(id={self.id}, target_level={self.target_level})>"


# Association Table for User Notification Seen Status
class UserNotificationStatus(Base):
    __tablename__ = "user_notification_status"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), primary_key=True)
    is_seen = Column(Boolean, default=False, nullable=False)
    seen_at = Column(DateTime(timezone=True), nullable=True) # Optional: timestamp when it was marked seen

    user = relationship("User", back_populates="seen_notifications_assoc")
    notification = relationship("Notification", back_populates="seen_by_users_assoc")

    def __repr__(self):
        return f"<UserNotificationStatus(user_id={self.user_id}, notification_id={self.notification_id}, is_seen={self.is_seen})>"

# Placeholder for DocumentSource if you plan to track uploaded documents separately in DB
# (Not strictly required for RAG if ChromaDB is the primary store for document metadata)
# class DocumentSource(Base):
#     __tablename__ = "document_sources"
#     id = Column(Integer, primary_key=True, index=True)
#     doc_internal_id = Column(String, unique=True, index=True, nullable=False)
#     original_filename = Column(String, nullable=False)
#     upload_time = Column(DateTime(timezone=True), server_default=func.now())
#     uploader_id = Column(Integer, ForeignKey("users.id"))
#     doc_access_target = Column(String, nullable=True) # e.g., public, level_1, admin_only

#     uploader = relationship("User")