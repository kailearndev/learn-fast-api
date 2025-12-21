
from fastapi import APIRouter
from modules.post.controller_public import router as public_router
from modules.post.controller import router as private_router
router = APIRouter(tags=["Bài viết"])

router.include_router(public_router, prefix="/posts")
router.include_router(private_router, prefix="/admin/posts")
