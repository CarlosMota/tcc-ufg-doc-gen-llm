from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from ...domain.search.service import MessageBusQueryNotifier, QueryService
from ...infrastructure.messaging import LoggingMessageBus
from ...infrastructure.vector_store import ChromaVectorRepository


@lru_cache
def get_query_service() -> QueryService:
    repository = ChromaVectorRepository()
    message_bus = LoggingMessageBus()
    notifier = MessageBusQueryNotifier(message_bus=message_bus)
    return QueryService(repository=repository, notifier=notifier)


ServiceDep = Annotated[QueryService, Depends(get_query_service)]
