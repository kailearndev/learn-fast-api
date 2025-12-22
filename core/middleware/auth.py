

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware

from core.supabase import supabase

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        
        auth_header = request.headers.get("Authorization")
        if auth_header  and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                res  = supabase.auth.get_user(token)
                request.state.user = res.user
            except Exception:
                # token sai hoac het han  -> chua login
                request.state.user = None
        
        response = await call_next(request)
        return response
