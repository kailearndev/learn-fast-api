from fastapi import APIRouter, HTTPException

from modules.post.schema import (
   
    PostPagingResponse,
    PostResponse
)
from modules.post.service import (
     list_all, get_by_slug
    )
router = APIRouter()

# Create a new post

# Get all posts
@router.get("/", response_model=PostPagingResponse)
def get_posts(page: int = 1, limit: int = 10, search: str = None):
    return list_all(page, limit, search)

@router.get("/{slug}",  response_model=PostResponse)
def get_post(slug: str):
    post = get_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
