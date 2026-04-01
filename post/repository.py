from abc import ABC, abstractmethod

from sqlalchemy import delete
from sqlalchemy.orm import Session

from db.model import Book, Sentence, User


class SentenceRepository(ABC):
    """Repository interface describing author persistence behavior."""

    @abstractmethod
    def find(self, id: int) -> Sentence:
        "해당 ID의 엔티티를 찾는 함수"

    @abstractmethod
    def create(self, post_data: dict) -> Sentence:
        """Persist a new author and return the stored entity."""

    @abstractmethod
    def update(self, sentence: Sentence) -> Sentence:
        """해당 엔티티를 업데이트하는 함수"""

    @abstractmethod
    def delete(self, sentence: Sentence):
        """해당 엔티티를 삭제하는 함수"""
    
class BookRepository(ABC):
    @abstractmethod
    def find(self, id: int) -> Book:
        "해당 ID의 엔티티를 찾는 함수"

class PostgresqlSentenceRepository(SentenceRepository):
    """SQLAlchemy-backed implementation of the AuthorRepository."""

    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> Sentence:
        return self.session.get(Sentence, id)

    def create(self, post_data: dict) -> Sentence:
        sentence = Sentence(**post_data)
        self.session.add(sentence)
        self.session.commit()
        self.session.refresh(sentence)
        return sentence
    
    def update(self, sentence: Sentence) -> Sentence:
        self.session.add(sentence)
        self.session.commit()
        self.session.refresh(sentence)
        return sentence
    
    def delete(self, sentence: Sentence):
        self.session.delete(sentence)
        self.session.commit()

class PostgresqlBookRepository(BookRepository):
    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> Book:
        return self.session.get(Book, id)
