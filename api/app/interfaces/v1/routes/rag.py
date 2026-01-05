from fastapi import APIRouter, HTTPException

from ....domain.search.models import RAGInput, RAGResponse
from ..dependencies import RAGServiceDep

router = APIRouter()


@router.post("/rag", response_model=RAGResponse)
def rag(query: RAGInput, service: RAGServiceDep) -> RAGResponse:
    try:
        return service.answer(query)
    except Exception as exc:  # pragma: no cover - fallback HTTP
        raise HTTPException(status_code=500, detail=str(exc)) from exc
