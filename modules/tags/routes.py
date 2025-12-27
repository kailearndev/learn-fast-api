
from fastapi import APIRouter
from modules.tags.controller_public import router as public_router
from modules.tags.controller import router as private_router
router = APIRouter(tags=["Thẻ"])

router.include_router(public_router, prefix="/tags")
router.include_router(private_router, prefix="/admin/tags")