import logging
from typing import List

import pytest

from app.application.services import QueryService
from app.domain.models import DocumentHit, QueryInput, QueryResult
from app.domain.repositories import MessageBus, VectorRepository


class FakeVectorRepository(VectorRepository):
    def __init__(self, hits: List[DocumentHit]) -> None:
        self._hits = hits
        self.last_query: QueryInput | None = None

    def query(self, query: QueryInput) -> QueryResult:
        self.last_query = query
        return QueryResult(query=query.text, hits=self._hits)


class DummyMessageBus(MessageBus):
    def __init__(self) -> None:
        self.published = []

    def publish(self, event: str, payload: dict) -> None:
        self.published.append((event, payload))


def test_query_service_returns_hits_and_publishes_event():
    hits = [
        DocumentHit(id="1", score=0.9, text="doc 1", metadata={"parser": "roslyn"}),
        DocumentHit(id="2", score=0.8, text="doc 2", metadata={"parser": "roslyn"}),
    ]
    repo = FakeVectorRepository(hits)
    bus = DummyMessageBus()
    service = QueryService(repository=repo, message_bus=bus)

    query_input = QueryInput(text="icms", top_k=2, namespace="SistemaFinanceiro.Domain")
    result = service.search(query_input)

    assert result.hits == hits
    assert repo.last_query == query_input
    assert bus.published == [("query_performed", {"query": "icms", "results": 2})]


def test_query_input_builds_filters():
    query_input = QueryInput(text="icms", parser="roslyn", namespace="ns")
    filters = query_input.filters()
    assert filters == {"namespace": "ns", "parser": "roslyn"}

