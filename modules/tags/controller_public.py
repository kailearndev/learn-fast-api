from fastapi import APIRouter, HTTPException

from modules.post.schema import PostPagingResponse
from modules.tags.schema import (
   
    TagsPagingResponse,
   
)
from modules.tags.service import (
        list_all
    )
router = APIRouter()

# Create a new post

# Get all posts
@router.get("/", response_model=TagsPagingResponse)
def get_tags(page: int = 1, limit: int = 10, search: str = None):
    return list_all(page, limit, search)

