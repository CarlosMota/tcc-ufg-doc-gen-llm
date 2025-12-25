from fastapi import APIRouter

from .... import config

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "version": config.APP_VERSION}
