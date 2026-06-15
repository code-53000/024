from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from ..models.specimen import IdentificationStatus


class IdentificationBase(BaseModel):
    status_after: IdentificationStatus
    comment: Optional[str] = None
    suggested_mineral_type: Optional[str] = Field(None, max_length=100)
    suggested_crystal_system: Optional[str] = Field(None, max_length=100)
    reference: Optional[str] = Field(None, max_length=500)
    confidence: Optional[int] = Field(None, ge=0, le=100)


class IdentificationCreate(IdentificationBase):
    specimen_id: int


class IdentificationResponse(IdentificationBase):
    id: int
    specimen_id: int
    identifier_id: int
    status_before: IdentificationStatus
    created_at: datetime

    class Config:
        from_attributes = True
