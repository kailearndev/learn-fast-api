from uuid import UUID
from core.supabase import supabase


def create_post(data: dict):
    
    tag_ids = data.pop("tags", [])
    res = supabase.table("posts").insert(data).execute()
    new_post = res.data[0]
    # Xử lý liên kết tags nếu có  
    # # 3. Nếu có tags, insert vào bảng trung gian post_tags
    if tag_ids:
        post_tag_data = [{"post_id": new_post["id"], "tag_id": tag_id} for tag_id in tag_ids] 
        supabase.table("post_tags").insert(post_tag_data).execute()
    return get_post_by_id(new_post["id"])
  

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
    return {
        "limit": limit,
        "page": page,
        "total": res.count,
        "data": res.data
    }
 
 
# Get post by ID
def get_post_by_id(post_id: UUID):
    res = supabase.table("posts").select("*, tags(id, name)").eq("id", str(post_id)).execute()
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
    res = supabase.table("posts").update(data).eq("id", str(post_id)).execute()
    return res.data[0] if res.data else None
# Delete post by ID

def delete_post(post_id: UUID):
    res = supabase.table("posts").delete().eq("id", str(post_id)).execute()
    return bool(res.data)