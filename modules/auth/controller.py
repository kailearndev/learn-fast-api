from fastapi import APIRouter, Depends
from core.dependencies.auth import require_user
from modules.auth.service import get_or_create_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/me")
def get_me(user = Depends(require_user)):
    """
    Trả về user hiện tại trong app (bảng users)
    """
    app_user = get_or_create_user(user)
    return app_user
