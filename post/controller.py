from unittest import result
from fastapi import APIRouter, Depends, status
from db.database import get_db
from db.model import Sentence
from sqlalchemy.orm import Session

from post.repository import (
    BookRepository,
    PostgresqlBookRepository,
    PostgresqlSentenceRepository,
    SentenceRepository,
)
from post.schemas import (
    AddSentenceRequest,
    AddSentenceResponse,
    DeleteSenteceRequest,
    DeleteSentenceResponse,
    ModifySenteceResponse,
    ModifySentenceRequest,
    PostChapterCreate,
    PostChapterResponse,
)
from post.service import PostService

router = APIRouter(prefix="/book", tags=["books"])

class PostController:
    def __init__(self, service: PostService):
        self.service = service

    def post(self, dto: PostChapterCreate):
        created: list[Sentence] = self.service.post_sentences(dto)
        result = list(map(lambda i : PostChapterResponse(i.id), created))
        return result
    
    def modify(self, dto: ModifySentenceRequest):
        return self.service.modify_sentence(dto)
    
    def add(self, dto: AddSentenceRequest):
        return self.service.add_sentence(dto)
    
    def delete_sentence(self, dto: DeleteSenteceRequest):
        self.service.delete_sentence(dto)

def get_sentence_repository(db: Session = Depends(get_db)) -> SentenceRepository:
    return PostgresqlSentenceRepository(db)


def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return PostgresqlBookRepository(db)


def get_post_service(
    sentence_repository: SentenceRepository = Depends(get_sentence_repository),
    book_repository: BookRepository = Depends(get_book_repository),
) -> PostService:
    return PostService(sentence_repository, book_repository)

def get_post_controller(
        service: PostService = Depends(get_post_service)
) -> PostController:
    return PostController(service)

@router.post("/chapter", response_model=list[PostChapterResponse], status_code=status.HTTP_201_CREATED)
def post_chapter(
    dto: PostChapterCreate, controller: PostController = Depends(get_post_controller)
) -> list[PostChapterResponse]:
    return controller.post(dto)

@router.patch("/chapter", response_class=ModifySenteceResponse, status_code=status.HTTP_200_OK)
def modify_sentence(
    dto: ModifySentenceRequest, controller: PostController = Depends(get_post_controller)
) -> ModifySenteceResponse:
    controller.modify(dto)
    return ModifySenteceResponse(result="성공적으로 문장이 수정되었습니다.")

@router.post("/sentence", response_class=AddSentenceResponse, status_code=status.HTTP_200_OK)
def post_sentence(
    dto: AddSentenceRequest, controller: PostController = Depends(get_post_controller)
) -> AddSentenceResponse:
    result = controller.add(dto)
    return AddSentenceResponse(id = result.id)

@router.delete("/sentence", response_class=DeleteSentenceResponse, status_code=status.HTTP_200_OK)
def delete_sentence(
    dto: DeleteSenteceRequest, controller: PostController = Depends(get_post_controller)
) -> DeleteSentenceResponse:
    controller.delete_sentence(dto)
    return DeleteSentenceResponse(result = "성공적으로 문장이 삭제되었습니다.")
