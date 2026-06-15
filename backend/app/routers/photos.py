from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List

from ..database import get_db
from ..models.user import User
from ..schemas.photo import PhotoResponse, BulkUploadResponse
from ..utils.security import get_current_active_user
from ..services.photo_service import PhotoService

router = APIRouter(prefix="/photos", tags=["照片管理"])


@router.get("/specimen/{specimen_id}", response_model=List[PhotoResponse])
def get_specimen_photos(
    specimen_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    return photo_service.get_by_specimen_id(specimen_id, current_user)


@router.get("/{photo_id}", response_model=PhotoResponse)
def get_photo(
    photo_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    photo = photo_service.get_by_id(photo_id, current_user)
    if not photo:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.post("/specimen/{specimen_id}", response_model=PhotoResponse)
async def upload_photo(
    specimen_id: int,
    file: UploadFile = File(...),
    is_primary: bool = Form(False),
    caption: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    return await photo_service.upload_single(
        specimen_id=specimen_id,
        file=file,
        current_user=current_user,
        is_primary=is_primary,
        caption=caption
    )


@router.post("/specimen/{specimen_id}/bulk", response_model=BulkUploadResponse)
async def bulk_upload_photos(
    specimen_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    return await photo_service.bulk_upload(
        specimen_id=specimen_id,
        files=files,
        current_user=current_user
    )


@router.put("/{photo_id}/primary", response_model=PhotoResponse)
def set_primary_photo(
    photo_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    return photo_service.set_primary(photo_id, current_user)


@router.put("/{photo_id}/caption", response_model=PhotoResponse)
def update_photo_caption(
    photo_id: int,
    caption: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    return photo_service.update_caption(photo_id, caption, current_user)


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(
    photo_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    photo_service = PhotoService(db)
    photo_service.delete(photo_id, current_user)
