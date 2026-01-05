from fastapi import APIRouter

from . import health, rag, search

router = APIRouter(prefix="/v1")
router.include_router(health.router)
router.include_router(rag.router)
router.include_router(search.router)

__all__ = ["router"]
