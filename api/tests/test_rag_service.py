from typing import List

from app.application.rag_service import RAGService
from app.domain.llm import LLMClient, LLMRequest, LLMResponse
from app.domain.search.models import DocumentHit, QueryResult, RAGInput
from app.domain.search.repositories import VectorRepository
from app.domain.search.service import QueryService


class FakeVectorRepository(VectorRepository):
    def __init__(self, hits: List[DocumentHit]) -> None:
        self._hits = hits
        self.last_query = None

    def query(self, query):
        self.last_query = query
        return QueryResult(query=query.text, hits=self._hits)


class FakeLLMClient(LLMClient):
    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.last_request: LLMRequest | None = None

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.last_request = request
        return LLMResponse(text=self.answer, raw={"prompt": request.prompt})


def test_rag_service_builds_prompt_and_calls_llm():
    hits = [
        DocumentHit(id="1", score=0.9, text="doc 1", metadata={}),
        DocumentHit(id="2", score=0.8, text="doc 2", metadata={}),
    ]
    repo = FakeVectorRepository(hits)
    query_service = QueryService(repository=repo)
    llm = FakeLLMClient(answer="resposta")
    rag_service = RAGService(query_service=query_service, llm_clients={"local": llm})

    rag_input = RAGInput(text="icms", top_k=2)
    response = rag_service.answer(rag_input)

    assert response.answer == "resposta"
    assert response.hits == hits
    assert llm.last_request is not None
    assert "Pergunta: icms" in llm.last_request.prompt
