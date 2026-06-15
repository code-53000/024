from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from pathlib import Path

from ..models.photo import Photo
from ..models.specimen import Specimen
from ..models.user import User
from ..schemas.photo import PhotoUploadResult, BulkUploadResponse
from ..utils.file_handler import save_upload_file
from ..config import settings


class PhotoService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, photo_id: int, current_user: User) -> Optional[Photo]:
        query = self.db.query(Photo).join(Specimen).filter(Photo.id == photo_id)
        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        return query.first()

    def get_by_specimen_id(self, specimen_id: int, current_user: User) -> List[Photo]:
        query = self.db.query(Photo).filter(Photo.specimen_id == specimen_id)
        if current_user.role != "admin":
            specimen = self.db.query(Specimen).filter(Specimen.id == specimen_id).first()
            if not specimen or specimen.owner_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
        return query.order_by(Photo.is_primary.desc(), Photo.sort_order.asc()).all()

    async def upload_single(
        self,
        specimen_id: int,
        file: UploadFile,
        current_user: User,
        is_primary: bool = False,
        caption: Optional[str] = None
    ) -> Photo:
        specimen = self.db.query(Specimen).filter(Specimen.id == specimen_id).first()
        if not specimen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specimen not found"
            )

        if current_user.role != "admin" and specimen.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        file_path, file_name, file_size, error = await save_upload_file(
            file,
            subdirectory="specimens",
            validate_image=True
        )

        if error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )

        if is_primary:
            self.db.query(Photo).filter(
                Photo.specimen_id == specimen_id,
                Photo.is_primary == True
            ).update({"is_primary": False})

        db_photo = Photo(
            specimen_id=specimen_id,
            file_path=file_path,
            file_name=file_name,
            original_name=file.filename,
            file_size=file_size,
            mime_type=file.content_type,
            is_primary=is_primary,
            caption=caption,
            upload_status="success",
            uploaded_by=current_user.id
        )
        self.db.add(db_photo)
        self.db.commit()
        self.db.refresh(db_photo)
        return db_photo

    async def bulk_upload(
        self,
        specimen_id: int,
        files: List[UploadFile],
        current_user: User
    ) -> BulkUploadResponse:
        specimen = self.db.query(Specimen).filter(Specimen.id == specimen_id).first()
        if not specimen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specimen not found"
            )

        if current_user.role != "admin" and specimen.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        results: List[PhotoUploadResult] = []
        success_count = 0
        failed_count = 0

        existing_photos = self.db.query(Photo).filter(
            Photo.specimen_id == specimen_id
        ).count()
        has_primary = existing_photos > 0

        for idx, file in enumerate(files):
            original_name = file.filename or "unknown"
            try:
                file_path, file_name, file_size, error = await save_upload_file(
                    file,
                    subdirectory="specimens",
                    validate_image=True
                )

                if error:
                    failed_count += 1
                    results.append(PhotoUploadResult(
                        success=False,
                        original_name=original_name,
                        error=error
                    ))
                    continue

                is_primary = (not has_primary and idx == 0)

                db_photo = Photo(
                    specimen_id=specimen_id,
                    file_path=file_path,
                    file_name=file_name,
                    original_name=original_name,
                    file_size=file_size,
                    mime_type=file.content_type,
                    is_primary=is_primary,
                    upload_status="success",
                    uploaded_by=current_user.id,
                    sort_order=idx
                )
                self.db.add(db_photo)
                self.db.flush()

                success_count += 1
                has_primary = True
                results.append(PhotoUploadResult(
                    success=True,
                    original_name=original_name,
                    file_name=file_name,
                    file_path=file_path,
                    photo_id=db_photo.id
                ))

            except Exception as e:
                failed_count += 1
                results.append(PhotoUploadResult(
                    success=False,
                    original_name=original_name,
                    error=str(e)
                ))

        self.db.commit()

        return BulkUploadResponse(
            specimen_id=specimen_id,
            total=len(files),
            success_count=success_count,
            failed_count=failed_count,
            results=results
        )

    def set_primary(self, photo_id: int, current_user: User) -> Photo:
        photo = self.get_by_id(photo_id, current_user)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )

        self.db.query(Photo).filter(
            Photo.specimen_id == photo.specimen_id,
            Photo.is_primary == True
        ).update({"is_primary": False})

        photo.is_primary = True
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def update_caption(
        self,
        photo_id: int,
        caption: str,
        current_user: User
    ) -> Photo:
        photo = self.get_by_id(photo_id, current_user)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )

        photo.caption = caption
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def delete(self, photo_id: int, current_user: User) -> None:
        photo = self.get_by_id(photo_id, current_user)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )

        try:
            file_path = Path(settings.UPLOAD_DIR) / photo.file_path.lstrip("/")
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass

        self.db.delete(photo)
        self.db.commit()

    def count(self) -> int:
        return self.db.query(Photo).count()
