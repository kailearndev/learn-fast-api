from fastapi import APIRouter, HTTPException
from uuid import UUID

from modules.post.schema import (
    PostResponse
)
from modules.post.service import (
     list_all, get_by_slug
    )
router = APIRouter()

# Create a new post

# Get all posts
@router.get("/", response_model=list[PostResponse])
def get_posts():
    return list_all()

@router.get("/{slug}",  response_model=PostResponse)
def get_post(slug: str):
    post = get_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
