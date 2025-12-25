from fastapi import APIRouter, HTTPException

from ....domain.search.models import QueryInput, QueryResult
from ..dependencies import ServiceDep

router = APIRouter()


@router.post("/search", response_model=QueryResult)
def search(query: QueryInput, service: ServiceDep) -> QueryResult:
    try:
        return service.search(query)
    except Exception as exc:  # pragma: no cover - fallback HTTP
        raise HTTPException(status_code=500, detail=str(exc)) from exc
