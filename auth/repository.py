from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from db.model import User


class AuthRepository(ABC):
    """Repository interface for authentication."""

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by email."""


class PostgresqlAuthRepository(AuthRepository):
    """SQLAlchemy-backed implementation of the AuthRepository."""

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()