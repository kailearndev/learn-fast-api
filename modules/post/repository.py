from uuid import UUID
from core.supabase import supabase
from fastapi.encoders import jsonable_encoder

from postgrest.exceptions import APIError

from fastapi import HTTPException, status


def create_post(data: dict):

    tags = data.pop("tags", [])
    clean_post_data = jsonable_encoder(data)
    try:
        res = supabase.table("posts").insert(data).execute()
        if not res.data:
            raise Exception("Failed to create post")
        new_post = res.data[0]
        new_post_id = new_post["id"]
        if tags:
            _add_tags_to_post(new_post_id, tags)
        return new_post
    except Exception as e:
        raise e


def _add_tags_to_post(post_id: str, tags: list):
    """
    Tạo các dòng liên kết trong bảng post_tags
    """
    relation_data = []
    for tag_item in tags:
        if isinstance(tag_item, dict):
            tag_id = str(tag_item.get("id"))
        else:
            tag_id = str(tag_item)
        relation_data.append({"post_id": post_id, "tag_id": tag_id})

    if relation_data:
        supabase.table("post_tags").insert(relation_data).execute()


# Get all posts with pagination and optional search
def get_posts(page: int = 1, limit: int = 10, search: str = None):
    # khởi tạo query
    query = supabase.table("posts").select("*, tags(id, name)", count="exact")
    # áp dụng phân trang nếu có
    if search:
        query = query.ilike("title", f"%{search}%")

    start = (page - 1) * limit
    end = start + limit - 1
    query = query.range(start, end)
    res = query.execute()
    return {"limit": limit, "page": page, "total": res.count, "data": res.data}


# Get post by ID
def get_post_by_id(post_id: UUID):
    res = (
        supabase.table("posts")
        .select("*, tags(id, name)")
        .eq("id", str(post_id))
        .execute()
    )
    if not res.data:
        return None
    return res.data[0]


# Get post by slug


def get_post_by_slug(slug: str):
    res = supabase.table("posts").select("*, tags(id, name)").eq("slug", slug).execute()
    if not res.data:
        return None
    return res.data[0]


# Update post by ID


def update_post(post_id: UUID, data: dict):
    # Tách tags ra khỏi data update
    # Lưu ý: Dùng .get() thay vì .pop() nếu bạn muốn giữ data gốc,
    # nhưng .pop() tiện hơn để clean data trước khi update post.
    tag_data = data.pop("tags", None)
    clean_post_data = jsonable_encoder(data)
    try:
        # Bước 1: Update thông tin bài viết (Title, Content...)
        # Chỉ update nếu còn dữ liệu (tránh trường hợp user chỉ gửi tags mà ko sửa bài)
        if clean_post_data:
            supabase.table("posts").update(clean_post_data).eq(
                "id", str(post_id)
            ).execute()
        # Bước 2: Update Tags (Nếu frontend có gửi trường tags lên)
        # Nếu tags_data là None -> Frontend không gửi -> Không làm gì cả
        # Nếu tags_data là [] -> Frontend gửi rỗng -> Xóa hết tags
        if tag_data is not None:
            _update_post_tags_relation(post_id, tag_data)
        # Bước 3: Trả về bài viết mới nhất kèm Tags để Frontend hiển thị luôn
        # Dùng select query embedding để lấy luôn tags
        res = (
            supabase.table("posts")
            .select("*, tags(id,name)")
            .eq("id", str(post_id))
            .single()
            .execute()
        )
        return res.data
    except APIError as e:
        error_msg = str(e)

        # Mã lỗi 23505 là Duplicate Key (Trùng lặp)
        if "23505" in error_msg or "posts_slug_key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,  # 409 Conflict
                detail={
                    "message": "Tiêu đề bài viết (Slug) đã tồn tại, vui lòng đổi tiêu đề khác.",
                    "code": "DUPLICATE_SLUG",
                    "field": "slug",
                },
            )
        raise e


def _update_post_tags_relation(post_id: UUID, new_tags: list):
    """
    Cập nhật Tags cho bài viết:
    1. Xóa hết liên kết cũ.
    2. Tạo liên kết mới.
    """
    str_post_id = str(post_id)
    supabase.table("post_tags").delete().eq("post_id", str_post_id).execute()

    if not new_tags:
        return

    relation_data = []
    for tag_item in new_tags:
        if isinstance(tag_item, dict):
            tag_id = str(tag_item.get("id"))
        else:
            tag_id = str(tag_item)
        relation_data.append({"post_id": str_post_id, "tag_id": tag_id})

    if relation_data:
        supabase.table("post_tags").insert(relation_data).execute()


# Delete post by ID


def delete_post(post_id: UUID):
    res = supabase.table("posts").delete().eq("id", str(post_id)).execute()
    return bool(res.data)
