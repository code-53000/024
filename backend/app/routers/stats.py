from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db
from ..models.user import User
from ..schemas.stats import StatsResponse
from ..utils.security import get_current_active_user
from ..services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["统计分析"])


@router.get("", response_model=StatsResponse)
def get_overall_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    stats_service = StatsService(db)
    return stats_service.get_overall_stats(current_user)
