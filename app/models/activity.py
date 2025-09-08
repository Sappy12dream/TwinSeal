# app/models/activity.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String, nullable=False)  # e.g., "upload", "download", "login"
    details = Column(String, nullable=True)  # optional extra info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
