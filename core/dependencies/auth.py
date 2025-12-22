from fastapi import Request,HTTPException, status

from core.supabase import supabase

def require_user(request: Request):
    if not request.state.user :
        raise HTTPException(401)
    return request.state.user

def require_admin(request: Request):
    user = require_user(request)

    res = supabase.table("users") \
        .select("role") \
        .eq("id", user.id) \
        .single() \
        .execute()

    if not res.data or res.data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user