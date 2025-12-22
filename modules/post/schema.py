from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class PostCreateDTO(BaseModel):
    title: str
    content: str
    is_public: bool = True
    slug: str 


class PostUpdateDTO(BaseModel):
    title : str | None = None
    slug : str | None = None
    content : str | None = None
    is_public : bool | None = None

class PostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime | None = None
