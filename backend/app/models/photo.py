from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


class UploadStatus(str):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    specimen_id = Column(Integer, ForeignKey("specimens.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    original_name = Column(String(200))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    is_primary = Column(Boolean, default=False, index=True)
    caption = Column(String(500))
    upload_status = Column(String(20), default="success")
    error_message = Column(Text)
    sort_order = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    specimen = relationship("Specimen", back_populates="photos")
