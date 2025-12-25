from typing import Optional

from ..interfaces.message_bus import MessageBus
from .models import QueryInput, QueryResult
from .repositories import VectorRepository


class QueryEventNotifier:
    """Define como um evento de consulta deve ser comunicado."""

    def notify_performed(self, query_input: QueryInput, result: QueryResult) -> None:
        raise NotImplementedError


class MessageBusQueryNotifier(QueryEventNotifier):
    """Publica eventos de consulta usando um MessageBus."""

    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus = message_bus

    def notify_performed(self, query_input: QueryInput, result: QueryResult) -> None:
        self.message_bus.publish(
            event="query_performed",
            payload={"query": query_input.text, "results": len(result.hits)},
        )


class QueryService:
    def __init__(
        self,
        repository: VectorRepository,
        notifier: Optional[QueryEventNotifier] = None,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def search(self, query_input: QueryInput) -> QueryResult:
        result = self.repository.query(query_input)
        if self.notifier:
            self.notifier.notify_performed(query_input, result)
        return result
