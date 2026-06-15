from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..models.specimen import Specimen, IdentificationStatus, CrystalSystem, AcquisitionMethod
from ..models.photo import Photo
from ..models.user import User
from ..schemas.stats import (
    StatsResponse,
    MineralStats,
    ProvinceStats,
    CrystalSystemStats,
    StatusStats,
    AcquisitionMethodStats
)


class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overall_stats(self, current_user: Optional[User] = None) -> StatsResponse:
        base_query_specimens = self.db.query(Specimen)
        base_query_photos = self.db.query(Photo).join(Specimen)

        if current_user and current_user.role != "admin":
            base_query_specimens = base_query_specimens.filter(
                Specimen.owner_id == current_user.id
            )
            base_query_photos = base_query_photos.filter(
                Specimen.owner_id == current_user.id
            )

        total_specimens = base_query_specimens.count()
        total_photos = base_query_photos.count()

        total_users = self.db.query(User).count() if (not current_user or current_user.role == "admin") else 1

        total_value = base_query_specimens.with_entities(
            func.sum(Specimen.price)
        ).scalar() or 0

        by_mineral = self._get_by_mineral(current_user)
        by_province = self._get_by_province(current_user)
        by_crystal_system = self._get_by_crystal_system(current_user)
        by_status = self._get_by_status(current_user)
        by_acquisition_method = self._get_by_acquisition_method(current_user)
        recent_specimens = self._get_recent_specimens(current_user)

        return StatsResponse(
            total_specimens=total_specimens,
            total_photos=total_photos,
            total_users=total_users,
            total_value=float(total_value),
            by_mineral=by_mineral,
            by_province=by_province,
            by_crystal_system=by_crystal_system,
            by_status=by_status,
            by_acquisition_method=by_acquisition_method,
            recent_specimens=recent_specimens
        )

    def _get_by_mineral(self, current_user: Optional[User]) -> List[MineralStats]:
        query = self.db.query(
            Specimen.mineral_type,
            func.count(Specimen.id).label("count")
        )

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = (
            query.filter(Specimen.mineral_type.isnot(None))
            .group_by(Specimen.mineral_type)
            .order_by(desc("count"))
            .limit(10)
            .all()
        )

        return [MineralStats(mineral_type=r[0], count=r[1]) for r in result]

    def _get_by_province(self, current_user: Optional[User]) -> List[ProvinceStats]:
        query = self.db.query(
            Specimen.province,
            func.count(Specimen.id).label("count")
        )

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = (
            query.filter(Specimen.province.isnot(None))
            .group_by(Specimen.province)
            .order_by(desc("count"))
            .limit(10)
            .all()
        )

        return [ProvinceStats(province=r[0], count=r[1]) for r in result]

    def _get_by_crystal_system(self, current_user: Optional[User]) -> List[CrystalSystemStats]:
        query = self.db.query(
            Specimen.crystal_system,
            func.count(Specimen.id).label("count")
        )

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = (
            query.filter(Specimen.crystal_system.isnot(None))
            .group_by(Specimen.crystal_system)
            .order_by(desc("count"))
            .all()
        )

        return [
            CrystalSystemStats(
                crystal_system=r[0].value if r[0] else "unknown",
                count=r[1]
            )
            for r in result
        ]

    def _get_by_status(self, current_user: Optional[User]) -> List[StatusStats]:
        query = self.db.query(
            Specimen.identification_status,
            func.count(Specimen.id).label("count")
        )

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = query.group_by(Specimen.identification_status).all()

        return [
            StatusStats(status=r[0].value if r[0] else "unknown", count=r[1])
            for r in result
        ]

    def _get_by_acquisition_method(self, current_user: Optional[User]) -> List[AcquisitionMethodStats]:
        query = self.db.query(
            Specimen.acquisition_method,
            func.count(Specimen.id).label("count")
        )

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = (
            query.filter(Specimen.acquisition_method.isnot(None))
            .group_by(Specimen.acquisition_method)
            .order_by(desc("count"))
            .all()
        )

        return [
            AcquisitionMethodStats(
                method=r[0].value if r[0] else "unknown",
                count=r[1]
            )
            for r in result
        ]

    def _get_recent_specimens(self, current_user: Optional[User]) -> List[Dict[str, Any]]:
        query = self.db.query(Specimen)

        if current_user and current_user.role != "admin":
            query = query.filter(Specimen.owner_id == current_user.id)

        result = (
            query.order_by(desc(Specimen.created_at))
            .limit(5)
            .all()
        )

        return [
            {
                "id": s.id,
                "specimen_no": s.specimen_no,
                "name": s.name,
                "mineral_type": s.mineral_type,
                "locality": s.locality,
                "identification_status": s.identification_status.value if s.identification_status else None,
                "created_at": s.created_at.isoformat()
            }
            for s in result
        ]
