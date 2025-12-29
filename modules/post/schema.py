from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from typing import List, Optional

from core.shema import PagingResponse


class TagReponse(BaseModel):
    id: UUID
    name: str


class PostCreateDTO(BaseModel):
    title: str
    content: str
    is_public: bool = True
    slug: str
    thumbnail: str | None = None
    tags: Optional[List[UUID]] = []
    summary: str | None = None


class PostUpdateDTO(BaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None
    is_public: bool | None = None
    thumbnail: str | None = None
    tags: Optional[List[UUID]] = []
    summary: str | None = None


class PostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime | None = None
    thumbnail: str
    tags: List[TagReponse] = []
    summary: str | None = None


class Config:
    from_attributes = True


PostPagingResponse = PagingResponse[PostResponse]
