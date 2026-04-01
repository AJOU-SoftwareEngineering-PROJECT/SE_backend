from typing import List

from db.model import Comment, SubComment
from comment.repository import CommentRepository


class CommentService:
    """Service layer for comment related operations."""

    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create_comment(self, comment_data: dict) -> Comment:
        """Persist a new comment into DB."""
        return self.repository.create(comment_data)

    def get_comments_by_sentence(self, sentence_id: int) -> List[Comment]:
        """Fetch comments for a sentence in descending order (newest first)."""
        return self.repository.get_by_sentence(sentence_id)

    def create_subcomment(self, subcomment_data: dict) -> SubComment:
        """Persist a new subcomment into DB."""
        return self.repository.create_subcomment(subcomment_data)

    def get_subcomments_by_comment(self, comment_id: int) -> List[SubComment]:
        """Fetch subcomments for a comment ordered by oldest first."""
        return self.repository.get_subcomments_by_comment(comment_id)

    def toggle_like(self, comment_id: int, user_id: int) -> bool:
        """Toggle like by user for a given comment and return new state."""
        return self.repository.toggle_like(comment_id, user_id)

    def count_likes(self, comment_id: int) -> int:
        """Return total like count for a comment."""
        return self.repository.count_likes(comment_id)
