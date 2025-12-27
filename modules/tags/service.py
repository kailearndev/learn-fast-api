from uuid import UUID

from modules.tags.repository import (
    create_tag,
    get_tags,
    get_tag_by_id,
    update_tag,
    delete_tag,
)


def create(data: dict):
    return create_tag(data)
def list_all(page: int = 1, limit: int = 10, search: str = None):
    return get_tags(page, limit, search)
def get_by_id(tag_id: UUID):
    return get_tag_by_id(tag_id)

def update(tag_id: UUID, data: dict):
    return update_tag(tag_id, data)
def delete(tag_id: UUID):
    return delete_tag(tag_id)