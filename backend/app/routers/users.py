from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserResponse, UserUpdate
from ..utils.security import get_current_active_user, get_current_admin_user
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.update(current_user.id, user_in)


@router.get("", response_model=List[UserResponse])
def get_all_users(
    current_user: Annotated[User, Depends(get_current_admin_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.update(user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user_service.delete(user_id)
