from uuid import UUID
from modules.post.repository import (
    create_post,
    get_posts,
    get_post_by_id,
    update_post,
    delete_post,
    get_post_by_slug
)

def create(data: dict):
    return create_post(data)
def list_all(page: int = 1, limit: int = 10, search: str = None):
    return get_posts(page, limit, search)
def get_by_id(post_id: UUID):
    return get_post_by_id(post_id)
def get_by_slug(slug: str):
    return get_post_by_slug(slug)
def update(post_id: UUID, data: dict):
    return update_post(post_id, data)
def delete(post_id: UUID):
    return delete_post(post_id)