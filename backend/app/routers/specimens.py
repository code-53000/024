from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List

from ..database import get_db
from ..models.user import User
from ..models.specimen import CrystalSystem, IdentificationStatus, AcquisitionMethod
from ..schemas.specimen import (
    SpecimenCreate,
    SpecimenUpdate,
    SpecimenResponse,
    SpecimenListResponse
)
from ..utils.security import get_current_active_user
from ..services.specimen_service import SpecimenService

router = APIRouter(prefix="/specimens", tags=["标本管理"])


@router.get("", response_model=SpecimenListResponse)
def get_specimens(
    current_user: Annotated[User, Depends(get_current_active_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    mineral_type: Optional[str] = None,
    locality: Optional[str] = None,
    province: Optional[str] = None,
    country: Optional[str] = None,
    crystal_system: Optional[CrystalSystem] = None,
    identification_status: Optional[IdentificationStatus] = None,
    acquisition_method: Optional[AcquisitionMethod] = None,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.get_list(
        current_user=current_user,
        page=page,
        page_size=page_size,
        keyword=keyword,
        mineral_type=mineral_type,
        locality=locality,
        province=province,
        country=country,
        crystal_system=crystal_system,
        identification_status=identification_status,
        acquisition_method=acquisition_method,
        owner_id=owner_id
    )


@router.get("/mineral-types", response_model=List[str])
def get_mineral_types(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.get_all_mineral_types(current_user)


@router.get("/provinces", response_model=List[str])
def get_provinces(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.get_all_provinces(current_user)


@router.get("/localities", response_model=List[str])
def get_localities(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.get_all_localities(current_user)


@router.get("/{specimen_id}", response_model=SpecimenResponse)
def get_specimen(
    specimen_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    specimen = specimen_service.get_by_id(specimen_id, current_user)
    if not specimen:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Specimen not found")
    return specimen


@router.post("", response_model=SpecimenResponse, status_code=status.HTTP_201_CREATED)
def create_specimen(
    specimen_in: SpecimenCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.create(specimen_in, current_user)


@router.put("/{specimen_id}", response_model=SpecimenResponse)
def update_specimen(
    specimen_id: int,
    specimen_in: SpecimenUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    return specimen_service.update(specimen_id, specimen_in, current_user)


@router.delete("/{specimen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specimen(
    specimen_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    specimen_service = SpecimenService(db)
    specimen_service.delete(specimen_id, current_user)
