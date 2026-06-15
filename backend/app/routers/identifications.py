from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..database import get_db
from ..models.user import User
from ..models.specimen import IdentificationStatus
from ..schemas.identification import IdentificationCreate, IdentificationResponse
from ..utils.security import get_current_active_user, get_current_admin_user
from ..services.identification_service import IdentificationService

router = APIRouter(prefix="/identifications", tags=["鉴定管理"])


@router.get("/specimen/{specimen_id}", response_model=List[IdentificationResponse])
def get_specimen_identifications(
    specimen_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    identification_service = IdentificationService(db)
    return identification_service.get_by_specimen_id(specimen_id, current_user)


@router.get("/pending", response_model=List[IdentificationResponse])
def get_pending_identifications(
    current_user: Annotated[User, Depends(get_current_active_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    identification_service = IdentificationService(db)
    items, _ = identification_service.get_pending_list(
        current_user=current_user,
        page=page,
        page_size=page_size
    )
    return items


@router.get("/allowed-transitions/{current_status}")
def get_allowed_transitions(
    current_status: IdentificationStatus,
    current_user: Annotated[User, Depends(get_current_admin_user)]
):
    identification_service = IdentificationService(None)
    transitions = identification_service.get_allowed_transitions(current_status)
    return {
        "current_status": current_status.value,
        "allowed_transitions": [t.value for t in transitions]
    }


@router.get("/{identification_id}", response_model=IdentificationResponse)
def get_identification(
    identification_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    identification_service = IdentificationService(db)
    identification = identification_service.get_by_id(identification_id)
    if not identification:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Identification record not found")
    return identification


@router.post("", response_model=IdentificationResponse, status_code=status.HTTP_201_CREATED)
def create_identification(
    identification_in: IdentificationCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    identification_service = IdentificationService(db)
    return identification_service.create(identification_in, current_user)


@router.delete("/{identification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identification(
    identification_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    identification_service = IdentificationService(db)
    identification_service.delete(identification_id, current_user)
