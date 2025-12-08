from typing import Optional

from ..domain.models import QueryInput, QueryResult
from ..domain.repositories import MessageBus, VectorRepository


class QueryService:
    def __init__(
        self,
        repository: VectorRepository,
        message_bus: Optional[MessageBus] = None,
    ) -> None:
        self.repository = repository
        self.message_bus = message_bus

    def search(self, query_input: QueryInput) -> QueryResult:
        result = self.repository.query(query_input)
        if self.message_bus:
            self.message_bus.publish(
                event="query_performed",
                payload={"query": query_input.text, "results": len(result.hits)},
            )
        return result

