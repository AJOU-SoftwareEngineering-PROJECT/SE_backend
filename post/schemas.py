
class PostChapterCreate:
    userId: int
    content: str
    bookId: int
    chapter: int

class PostChapterResponse:
    idList: list[int]

class ModifySentenceRequest: 
    sentenceId: int
    content: str

class ModifySenteceResponse:
    result: str

class AddSentenceRequest:
    beforeId: int
    afterId: int
    bookId: int
    content: str

class AddSentenceResponse:
    id: int

class DeleteSenteceRequest:
    sentenceId: int
    beforeId: int

class DeleteSentenceResponse:
    result: str