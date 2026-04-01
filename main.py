from fastapi import FastAPI

from author.controller import router as author_router
from comment.controller import router as comment_router, subcomment_router
from db.database import init_db

app = FastAPI(title="Author Service")
app.include_router(author_router)
app.include_router(comment_router)
app.include_router(subcomment_router)


@app.on_event("startup")
def on_startup():
    """Ensure all database tables exist before serving requests."""
    init_db()
