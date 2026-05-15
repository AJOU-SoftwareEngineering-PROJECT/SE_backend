from fastapi import FastAPI

from author.controller import router as author_router
from comment.controller import router as comment_router, subcomment_router
from scrap.controller import router as scrap_router, user_router as scrap_user_router
from alarm.controller import router as alarm_router
from post.controller import router as post_router
from auth.controller import router as auth_router
from db.database import init_db

app = FastAPI(title="Author Service")
app.include_router(author_router)
app.include_router(comment_router)
app.include_router(subcomment_router)
app.include_router(scrap_router)
app.include_router(scrap_user_router)
app.include_router(alarm_router)
app.include_router(post_router)
app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    """Ensure all database tables exist before serving requests."""
    init_db()
