import re
from db.model import Sentence
from post.repository import BookRepository, SentenceRepository
from post.schemas import AddSentenceRequest, DeleteSenteceRequest, ModifySentenceRequest, PostChapterCreate


class PostService:
    def __init__(self, sentence_repository: SentenceRepository, book_repository: BookRepository):
        self.sentence_repository = sentence_repository
        self.book_repository = book_repository
    
    def post_sentences(self, dto: PostChapterCreate) -> list[Sentence]:
        
        sentences = dto.content
        bookId = dto.bookId
        chapter = dto.chapter
        saved_sentences = []

        # 빈 문자열 제거
        split_sentences = [
            s.strip()
            for s in re.split(r"[.?]", sentences)
            if s.strip()
        ]

        for sentence in split_sentences:
            saved = self.sentence_repository.create({
                "chapter": chapter,
                "content": sentence,
                "book_id": bookId,
            })
            saved_sentences.append(saved)

        # 마지막 문장은 다음 문장이 없으므로 len - 1까지만
        for i in range(len(saved_sentences) - 1):
            saved_sentences[i].after_id = saved_sentences[i + 1].id
            self.sentence_repository.update(saved_sentences[i])

        return saved_sentences
            
    def modify_sentence(self, dto: ModifySentenceRequest) -> Sentence:
        sentence = self.sentence_repository.find(dto.sentenceId)
        sentence.content = dto.content
        return self.sentence_repository.update(sentence)
    
    def add_sentence(self, dto: AddSentenceRequest) -> Sentence:
        book = self.book_repository.find(dto.bookId)
        if book is None:
            raise ValueError("Book not found")

        before = self.sentence_repository.find(dto.beforeId)
        if before is None:
            raise ValueError("Before sentence not found")

        sentence = {
            "book_id": book.id,
            "chapter": before.chapter,
            "content": dto.content,
            "after_id": dto.afterId,
        }
        saved_sentence = self.sentence_repository.create(sentence)

        before.after_id = saved_sentence.id
        self.sentence_repository.update(before)

        return saved_sentence
    
    def delete_sentence(self, dto: DeleteSenteceRequest):
        before = self.sentence_repository.find(dto.beforeId)
        sentence = self.sentence_repository.find(dto.sentenceId)
        before.after_id = sentence.after_id

        self.sentence_repository.update(before)
        self.sentence_repository.delete(sentence)

