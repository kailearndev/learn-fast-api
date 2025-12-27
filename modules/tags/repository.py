from uuid import UUID

from fastapi import HTTPException , status
from postgrest import APIError
from slugify import slugify
from core.shema import ErrorDetail, ErrorResponse
from core.supabase import supabase


def create_tag(data: dict):
    try:
        # Gọi Supabase
        res = supabase.table("tags").insert(data).execute()
        
        # Nếu thành công, trả về data
        if res.data:
            return res.data[0]
        return None

    except APIError as e:
        # Kiểm tra lỗi trùng lặp (Mã 23505 của Postgres)
        if "23505" in str(e) or "duplicate key" in str(e):
            # TẠI ĐÂY: Ném lỗi thẳng ra ngoài. 
            # FastAPI sẽ tự bắt lỗi này và trả về JSON cho F.E
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
           detail=ErrorResponse(
            message="Lỗi thao tác dữ liệu",
            code="DATA_CONFLICT",
            data=ErrorDetail(   # <--- Lồng object data vào đây
               message=f"Tag '{data.get('name')}' đã tồn tại (slug: {data.get('slug')}).",
                code="DUPLICATE_NAME")).model_dump())
        
        # Nếu là lỗi khác (ví dụ mất mạng), ném tiếp để log lại hoặc xử lý sau
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail=ErrorResponse(
            message="Lỗi hệ thống",
            code="INTERNAL_SERVER_ERROR",
            data=ErrorDetail()).model_dump())
def get_tags(page: int = 1, limit: int = 10, search: str = None):
    # khởi tạo query
    query = supabase.table("tags").select("*", count="exact")
    # áp dụng phân trang nếu có
    if search:
        query = query.ilike("name", f"%{search}%")
    
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
    # res = supabase.table("posts").select("*").execute()
def get_tag_by_id(tag_id: UUID):
    res = supabase.table("tags").select("*").eq("id", str(tag_id)).execute()
    if not res.data:
            return None
    return res.data[0]



def update_tag(tag_id: UUID, data: dict):
    try:
        res = supabase.table("tags").update(data).eq("id", str(tag_id)).execute()
        if res.data:
            return res.data[0]
        return None
    except APIError as e:
        # Kiểm tra lỗi trùng lặp (Mã 23505 của Postgres)
        if "23505" in str(e) or "duplicate key" in str(e):
            # TẠI ĐÂY: Ném lỗi thẳng ra ngoài. 
            # FastAPI sẽ tự bắt lỗi này và trả về JSON cho F.E
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
           detail=ErrorResponse(
            message="Lỗi thao tác dữ liệu",
            code="DATA_CONFLICT",
            data=ErrorDetail(   # <--- Lồng object data vào đây
               message=f"Tag '{data.get('name')}' đã tồn tại (slug: {data.get('slug')}).",
                code="DUPLICATE_NAME")).model_dump())
        
        # Nếu là lỗi khác (ví dụ mất mạng), ném tiếp để log lại hoặc xử lý sau
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail=ErrorResponse(
            message="Lỗi hệ thống",
            code="INTERNAL_SERVER_ERROR",
            data=ErrorDetail()).model_dump())
def delete_tag(tag_id: UUID):
    res = supabase.table("tags").delete().eq("id", str(tag_id)).execute()
    return bool(res.data)