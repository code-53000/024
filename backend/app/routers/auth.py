from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db
from ..schemas.user import UserCreate, UserLogin, Token, UserResponse
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create(user_in)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.authenticate(user_in)
