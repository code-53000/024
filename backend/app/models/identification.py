from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base
from .specimen import IdentificationStatus


class Identification(Base):
    __tablename__ = "identifications"

    id = Column(Integer, primary_key=True, index=True)
    specimen_id = Column(Integer, ForeignKey("specimens.id"), nullable=False, index=True)
    identifier_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status_before = Column(Enum(IdentificationStatus), nullable=False)
    status_after = Column(Enum(IdentificationStatus), nullable=False)
    comment = Column(Text)
    suggested_mineral_type = Column(String(100))
    suggested_crystal_system = Column(String(100))
    reference = Column(String(500))
    confidence = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    specimen = relationship("Specimen", back_populates="identifications")
    identifier = relationship("User", back_populates="identifications")
