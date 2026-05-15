from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.repository import PostgresqlAuthRepository
from auth.schemas import LoginRequest, TokenResponse
from auth.service import AuthService
from db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    repository = PostgresqlAuthRepository(db)
    service = AuthService(repository)
    try:
        access_token = service.authenticate_user(request.email, request.password)
        return TokenResponse(access_token=access_token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )