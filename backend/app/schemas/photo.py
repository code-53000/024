from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PhotoBase(BaseModel):
    caption: Optional[str] = None
    is_primary: bool = False


class PhotoResponse(PhotoBase):
    id: int
    specimen_id: int
    file_path: str
    file_name: str
    original_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    upload_status: str
    error_message: Optional[str] = None
    sort_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhotoUploadResult(BaseModel):
    success: bool
    original_name: str
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    photo_id: Optional[int] = None
    error: Optional[str] = None


class BulkUploadResponse(BaseModel):
    specimen_id: int
    total: int
    success_count: int
    failed_count: int
    results: List[PhotoUploadResult]
