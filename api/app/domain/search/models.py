from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryInput(BaseModel):
    text: str = Field(..., description="Texto para buscar no vetor.")
    top_k: int = Field(5, ge=1, le=50, description="Quantidade de resultados.")
    namespace: Optional[str] = None
    parser: Optional[str] = None

    def filters(self) -> Dict[str, Any]:
        where: Dict[str, Any] = {}
        if self.namespace:
            where["namespace"] = self.namespace
        if self.parser:
            where["parser"] = self.parser
        return where


class DocumentHit(BaseModel):
    id: str
    score: float
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryResult(BaseModel):
    query: str
    hits: List[DocumentHit] = Field(default_factory=list)


class RAGResponse(BaseModel):
    query: str
    answer: str
    hits: List[DocumentHit]


class RAGInput(QueryInput):
    provider: Optional[str] = Field(
        None, description="Provedor do modelo LLM (opcional; usa default)."
    )
    model: Optional[str] = Field(None, description="Sobrescreve o modelo do provedor.")
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1)
