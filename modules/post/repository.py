from uuid import UUID
from core.supabase import supabase


def create_post(data: dict):
    res = supabase.table("posts").insert(data).execute()
    return res.data[0]
def get_posts():
    res = supabase.table("posts").select("*").execute()
    return res.data
def get_post_by_id(post_id: UUID):
    res = supabase.table("posts").select("*").eq("id", str(post_id)).execute()
    if not res.data:
            return None
    return res.data

def get_post_by_slug(slug: str):
    res = supabase.table("posts").select("*").eq("slug", slug).execute()
    if not res.data:
            return None
    return res.data[0]
        
    
    


def update_post(post_id: UUID, data: dict):
    res = supabase.table("posts").update(data).eq("id", str(post_id)).execute()
    return res.data[0] if res.data else None
def delete_post(post_id: UUID):
    res = supabase.table("posts").delete().eq("id", str(post_id)).execute()
    return bool(res.data)