from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from datetime import datetime

from ..models.specimen import (
    Specimen,
    IdentificationStatus,
    CrystalSystem,
    AcquisitionMethod
)
from ..models.user import User
from ..schemas.specimen import SpecimenCreate, SpecimenUpdate, SpecimenListResponse


class SpecimenService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_specimen_no(self) -> str:
        today = datetime.now()
        prefix = f"SP{today.strftime('%Y%m')}"
        last_specimen = (
            self.db.query(Specimen)
            .filter(Specimen.specimen_no.like(f"{prefix}%"))
            .order_by(Specimen.specimen_no.desc())
            .first()
        )
        if last_specimen:
            seq = int(last_specimen.specimen_no[-4:]) + 1
        else:
            seq = 1
        return f"{prefix}{seq:04d}"

    def get_by_id(self, specimen_id: int, current_user: User) -> Optional[Specimen]:
        query = self.db.query(Specimen).filter(Specimen.id == specimen_id)
        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        return query.first()

    def get_list(
        self,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None,
        mineral_type: Optional[str] = None,
        locality: Optional[str] = None,
        province: Optional[str] = None,
        country: Optional[str] = None,
        crystal_system: Optional[CrystalSystem] = None,
        identification_status: Optional[IdentificationStatus] = None,
        acquisition_method: Optional[AcquisitionMethod] = None,
        owner_id: Optional[int] = None
    ) -> SpecimenListResponse:
        query = self.db.query(Specimen)

        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        elif owner_id is not None:
            query = query.filter(Specimen.owner_id == owner_id)

        if keyword:
            query = query.filter(
                or_(
                    Specimen.name.contains(keyword),
                    Specimen.specimen_no.contains(keyword),
                    Specimen.mineral_type.contains(keyword),
                    Specimen.locality.contains(keyword),
                    Specimen.description.contains(keyword)
                )
            )
        if mineral_type:
            query = query.filter(Specimen.mineral_type == mineral_type)
        if locality:
            query = query.filter(Specimen.locality.contains(locality))
        if province:
            query = query.filter(Specimen.province == province)
        if country:
            query = query.filter(Specimen.country == country)
        if crystal_system:
            query = query.filter(Specimen.crystal_system == crystal_system)
        if identification_status:
            query = query.filter(Specimen.identification_status == identification_status)
        if acquisition_method:
            query = query.filter(Specimen.acquisition_method == acquisition_method)

        total = query.count()
        items = (
            query.order_by(Specimen.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return SpecimenListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )

    def create(self, specimen_in: SpecimenCreate, current_user: User) -> Specimen:
        specimen_no = specimen_in.specimen_no or self._generate_specimen_no()

        if specimen_in.specimen_no:
            existing = self.db.query(Specimen).filter(Specimen.specimen_no == specimen_no).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Specimen number already exists"
                )

        db_specimen = Specimen(
            **specimen_in.model_dump(exclude={"specimen_no"}),
            specimen_no=specimen_no,
            owner_id=current_user.id,
            identification_status=IdentificationStatus.PENDING
        )
        self.db.add(db_specimen)
        self.db.commit()
        self.db.refresh(db_specimen)
        return db_specimen

    def update(
        self,
        specimen_id: int,
        specimen_in: SpecimenUpdate,
        current_user: User
    ) -> Specimen:
        db_specimen = self.get_by_id(specimen_id, current_user)
        if not db_specimen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specimen not found"
            )

        if current_user.role != "admin" and db_specimen.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        update_data = specimen_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_specimen, field, value)

        self.db.commit()
        self.db.refresh(db_specimen)
        return db_specimen

    def delete(self, specimen_id: int, current_user: User) -> None:
        db_specimen = self.get_by_id(specimen_id, current_user)
        if not db_specimen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specimen not found"
            )

        if current_user.role != "admin" and db_specimen.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        self.db.delete(db_specimen)
        self.db.commit()

    def get_all_mineral_types(self, current_user: User) -> List[str]:
        query = self.db.query(Specimen.mineral_type).distinct()
        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        result = query.filter(Specimen.mineral_type.isnot(None)).all()
        return [r[0] for r in result]

    def get_all_localities(self, current_user: User) -> List[str]:
        query = self.db.query(Specimen.locality).distinct()
        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        result = query.filter(Specimen.locality.isnot(None)).all()
        return [r[0] for r in result]

    def get_all_provinces(self, current_user: User) -> List[str]:
        query = self.db.query(Specimen.province).distinct()
        if current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        result = query.filter(Specimen.province.isnot(None)).all()
        return [r[0] for r in result]

    def count(self, current_user: Optional[User] = None) -> int:
        query = self.db.query(Specimen)
        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        return query.count()

    def total_value(self, current_user: Optional[User] = None) -> float:
        from sqlalchemy import func
        query = self.db.query(func.sum(Specimen.price))
        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)
        result = query.scalar()
        return float(result or 0)
