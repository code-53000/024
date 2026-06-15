from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.identification import Identification
from ..models.specimen import Specimen, IdentificationStatus
from ..models.user import User, UserRole
from ..schemas.identification import IdentificationCreate, IdentificationResponse


class IdentificationService:
    def __init__(self, db: Session):
        self.db = db

    ALLOWED_TRANSITIONS = {
        IdentificationStatus.PENDING: [
            IdentificationStatus.CONFIRMED,
            IdentificationStatus.DISPUTED
        ],
        IdentificationStatus.CONFIRMED: [
            IdentificationStatus.DISPUTED,
            IdentificationStatus.PENDING
        ],
        IdentificationStatus.DISPUTED: [
            IdentificationStatus.CONFIRMED,
            IdentificationStatus.PENDING
        ]
    }

    def _validate_transition(
        self,
        current_status: IdentificationStatus,
        target_status: IdentificationStatus
    ) -> bool:
        return target_status in self.ALLOWED_TRANSITIONS.get(current_status, [])

    def get_by_id(self, identification_id: int) -> Optional[Identification]:
        return self.db.query(Identification).filter(Identification.id == identification_id).first()

    def get_by_specimen_id(
        self,
        specimen_id: int,
        current_user: User
    ) -> List[Identification]:
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

        return (
            self.db.query(Identification)
            .filter(Identification.specimen_id == specimen_id)
            .order_by(Identification.created_at.desc())
            .all()
        )

    def get_pending_list(
        self,
        current_user: User,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Identification], int]:
        query = self.db.query(Identification).join(Specimen).filter(
            Specimen.identification_status == IdentificationStatus.PENDING
        )

        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        total = query.count()
        items = (
            query.order_by(Identification.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def create(
        self,
        identification_in: IdentificationCreate,
        current_user: User
    ) -> Identification:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can perform identification"
            )

        specimen = self.db.query(Specimen).filter(
            Specimen.id == identification_in.specimen_id
        ).first()
        if not specimen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specimen not found"
            )

        current_status = specimen.identification_status
        target_status = identification_in.status_after

        if not self._validate_transition(current_status, target_status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status.value} to {target_status.value}"
            )

        db_identification = Identification(
            **identification_in.model_dump(),
            identifier_id=current_user.id,
            status_before=current_status
        )
        self.db.add(db_identification)

        specimen.identification_status = target_status

        self.db.commit()
        self.db.refresh(db_identification)
        return db_identification

    def get_allowed_transitions(
        self,
        current_status: IdentificationStatus
    ) -> List[IdentificationStatus]:
        return self.ALLOWED_TRANSITIONS.get(current_status, [])

    def delete(self, identification_id: int, current_user: User) -> None:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete identification records"
            )

        identification = self.get_by_id(identification_id)
        if not identification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Identification record not found"
            )

        self.db.delete(identification)
        self.db.commit()
