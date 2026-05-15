from pydantic import BaseModel, ConfigDict

from db.model import Gender


class AuthorBase(BaseModel):
    name: str
    gender: Gender
    age: int
    intro: str
    email: str


class AuthorCreate(AuthorBase):
    """Payload required to register an author."""
    password: str


class AuthorResponse(AuthorBase):
    """Representation returned by the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)
