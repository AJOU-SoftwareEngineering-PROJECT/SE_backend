from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.repository import AuthRepository
from core.security import create_access_token, verify_password
from db.model import User


class AuthService:
    """Service for handling authentication logic."""

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def authenticate_user(self, email: str, password: str) -> str:
        """Authenticate user and return access token."""
        user = self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"user_id": user.id})
        return access_token