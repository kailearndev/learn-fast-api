from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from fastapi.security import HTTPBearer

from core.dependencies.auth import require_user
from modules.tags.schema import (
    TagsPagingResponse, TagsCreateDTO, TagsUpdateDTO, TagsResponse
)
from modules.tags.service import (
    create, list_all, get_by_id, update, delete
    )

security = HTTPBearer()

router = APIRouter(
     dependencies=[Depends(require_user),
                   Depends(security)],
)

# Create a new post
@router.post("/", response_model=TagsResponse)
def create_tag (payload: TagsCreateDTO): 
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid payload")
    if not payload.name:
        raise HTTPException(status_code=400, detail="Name is required")
    
    post = create(payload.model_dump())
    return post

# Get all posts
@router.get("/", response_model=TagsPagingResponse )
def get_tags( page: int = 1, limit: int = 10, search: str = None):
    return list_all(page, limit, search)
# Get a tag by ID
@router.get("/{tag_id}", response_model=TagsResponse)
def get_tag_by_id(tag_id: UUID):
    p = get_by_id(tag_id)
    if not p:
        raise HTTPException(status_code=404, detail="Tag not found")
    return p


# Update a tag by ID
@router.put("/{tag_id}", response_model=TagsResponse)
def update_tag(tag_id: UUID, payload: TagsUpdateDTO):
    tag = update(
        tag_id,
        payload.model_dump(exclude_unset=True)
    )
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
# Delete a post by ID
@router.delete("/{post_id}")
def delete_post(post_id: UUID):
    success = delete(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
        
  