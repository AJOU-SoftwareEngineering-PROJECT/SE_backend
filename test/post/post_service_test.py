import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from db.model import Book, Gender, Sentence, User
from post.repository import PostgresqlBookRepository, PostgresqlSentenceRepository
from post.schemas import (
    AddSentenceRequest,
    DeleteSenteceRequest,
    ModifySentenceRequest,
    PostChapterCreate,
)
from post.service import PostService


@pytest.fixture()
def session():
    """Create an isolated in-memory DB session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def sentence_repository(session):
    return PostgresqlSentenceRepository(session)


@pytest.fixture()
def book_repository(session):
    return PostgresqlBookRepository(session)


@pytest.fixture()
def service(sentence_repository, book_repository):
    return PostService(sentence_repository, book_repository)


def make_post_chapter_dto(content: str) -> PostChapterCreate:
    dto = PostChapterCreate()
    dto.userId = 1
    dto.content = content
    dto.bookId = 42
    dto.chapter = 3
    return dto


def make_modify_sentence_dto(sentence_id: int, content: str) -> ModifySentenceRequest:
    dto = ModifySentenceRequest()
    dto.sentenceId = sentence_id
    dto.content = content
    return dto


def make_add_sentence_dto(before_id: int, after_id: int, book_id: int, content: str) -> AddSentenceRequest:
    dto = AddSentenceRequest()
    dto.beforeId = before_id
    dto.afterId = after_id
    dto.bookId = book_id
    dto.content = content
    return dto


def make_delete_sentence_dto(before_id: int, sentence_id: int) -> DeleteSenteceRequest:
    dto = DeleteSenteceRequest()
    dto.beforeId = before_id
    dto.sentenceId = sentence_id
    return dto


def test_post_sentences_persists_each_sentence(service, session):
    dto = make_post_chapter_dto("첫 문장. 두 번째 문장? 마지막 문장.")

    created = service.post_sentences(dto)

    assert len(created) == 3
    assert [s.content for s in created] == [
        "첫 문장",
        "두 번째 문장",
        "마지막 문장",
    ]
    assert all(sentence.book_id == dto.bookId for sentence in created)
    assert all(sentence.chapter == dto.chapter for sentence in created)

    stored = session.query(Sentence).order_by(Sentence.id).all()
    assert len(stored) == 3


def test_post_sentences_links_after_ids(service, session):
    dto = make_post_chapter_dto("A.  B?C.")

    service.post_sentences(dto)

    stored = session.query(Sentence).order_by(Sentence.id).all()

    assert stored[0].after_id == stored[1].id
    assert stored[1].after_id == stored[2].id
    assert stored[2].after_id is None


def test_modify_sentence_updates_content(service, session):
    sentence = Sentence(chapter=1, content="original", book_id=5)
    session.add(sentence)
    session.commit()

    dto = make_modify_sentence_dto(sentence.id, "updated sentence")

    updated = service.modify_sentence(dto)

    assert updated.id == sentence.id
    assert updated.content == "updated sentence"

    refreshed = session.get(Sentence, sentence.id)
    assert refreshed.content == "updated sentence"


def test_add_sentence_creates_new_sentence_and_updates_links(service, session):
    user = User(name="Kim", gender=Gender.MALE, age=30, intro="intro", email="kim@example.com")
    session.add(user)
    session.commit()

    book = Book(name="Book 1", author_id=user.id)
    session.add(book)
    session.commit()

    before = Sentence(chapter=1, content="before", book_id=book.id, after_id=None)
    after = Sentence(chapter=1, content="after", book_id=book.id, after_id=None)
    session.add_all([before, after])
    session.commit()

    dto = make_add_sentence_dto(before.id, after.id, book.id, "inserted")

    created = service.add_sentence(dto)

    assert created.content == "inserted"
    assert created.after_id == after.id
    assert created.book_id == book.id

    reloaded_before = session.get(Sentence, before.id)
    assert reloaded_before.after_id == created.id


def test_delete_sentence_unlinks_before_and_removes_sentence(service, session):
    user = User(name="Han", gender=Gender.FEMALE, age=28, intro="intro", email="han@example.com")
    session.add(user)
    session.commit()

    book = Book(name="Mystery", author_id=user.id)
    session.add(book)
    session.commit()

    before = Sentence(chapter=1, content="before", book_id=book.id)
    target = Sentence(chapter=1, content="delete me", book_id=book.id)
    after = Sentence(chapter=1, content="after", book_id=book.id)
    session.add_all([before, target, after])
    session.commit()

    before.after_id = target.id
    target.after_id = after.id
    session.add_all([before, target])
    session.commit()

    dto = make_delete_sentence_dto(before.id, target.id)

    service.delete_sentence(dto)

    refreshed_before = session.get(Sentence, before.id)
    assert refreshed_before.after_id == after.id

    assert session.get(Sentence, target.id) is None
