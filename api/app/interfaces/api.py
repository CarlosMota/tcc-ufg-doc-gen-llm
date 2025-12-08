from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from .. import config
from ..application.services import QueryService
from ..domain.models import QueryInput, QueryResult
from ..infrastructure.messaging import LoggingMessageBus
from ..infrastructure.vector_repository import ChromaVectorRepository


@lru_cache
def get_service() -> QueryService:
    repository = ChromaVectorRepository()
    message_bus = LoggingMessageBus()
    return QueryService(repository=repository, message_bus=message_bus)


ServiceDep = Annotated[QueryService, Depends(get_service)]

app = FastAPI(
    title="TCC RAG API",
    version=config.APP_VERSION,
    description="API para consultas a documentos vetoriais (Chroma).",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": config.APP_VERSION}


@app.post("/search", response_model=QueryResult)
def search(query: QueryInput, service: ServiceDep) -> QueryResult:
    try:
        return service.search(query)
    except Exception as exc:  # pragma: no cover - fallback HTTP
        raise HTTPException(status_code=500, detail=str(exc)) from exc

