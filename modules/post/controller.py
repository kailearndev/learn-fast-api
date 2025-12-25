from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from fastapi.security import HTTPBearer

from core.dependencies.auth import require_user
from modules.post.schema import (
    PostCreateDTO, PostUpdateDTO, PostResponse
)
from modules.post.service import (
    create, list_all, get_by_id, update, delete, get_by_slug
    )

security = HTTPBearer()

router = APIRouter(
     dependencies=[Depends(require_user),
                   Depends(security)],
     
)

# Create a new post
@router.post("/", response_model=PostResponse)
def create_post (payload: PostCreateDTO): 
    slug_check = get_by_slug(payload.slug)
    if slug_check:
        raise HTTPException(status_code=400, detail="Slug already exists")
    post = create(payload.model_dump())
    return post

# Get all posts
@router.get("/", response_model=list[PostResponse])
def get_posts():
    return list_all()
# Get a post by ID
@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id(post_id: UUID):
    p = get_by_id(post_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p


# Update a post by ID
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: UUID, payload: PostUpdateDTO):
    post = update(
        post_id,
        payload.model_dump(exclude_unset=True)
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
# Delete a post by ID
@router.delete("/{post_id}")
def delete_post(post_id: UUID):
    success = delete(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
        
  