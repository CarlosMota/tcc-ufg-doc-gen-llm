from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from ... import config
from ...application.rag_service import RAGService
from ...domain.search.service import MessageBusQueryNotifier, QueryService
from ...infrastructure.llm import ExternalLLMClient, LocalLLMClient
from ...infrastructure.messaging import LoggingMessageBus
from ...infrastructure.vector_store import ChromaVectorRepository


@lru_cache
def get_query_service() -> QueryService:
    repository = ChromaVectorRepository()
    message_bus = LoggingMessageBus()
    notifier = MessageBusQueryNotifier(message_bus=message_bus)
    return QueryService(repository=repository, notifier=notifier)


ServiceDep = Annotated[QueryService, Depends(get_query_service)]


@lru_cache
def get_rag_service() -> RAGService:
    query_service = get_query_service()
    llm_clients = {}
    for provider in config.LLM_PROVIDERS:
        settings = config.get_llm_provider_settings(provider)
        if not settings["base_url"]:
            raise ValueError(f"LLM_{provider.upper()}_BASE_URL não configurado.")
        if settings["api_key"]:
            llm_clients[provider] = ExternalLLMClient(
                base_url=settings["base_url"],
                api_key=settings["api_key"],
                model=settings["model"],
                timeout=config.LLM_TIMEOUT_SECONDS,
            )
        else:
            llm_clients[provider] = LocalLLMClient(
                base_url=settings["base_url"],
                model=settings["model"],
                timeout=config.LLM_TIMEOUT_SECONDS,
            )
    return RAGService(
        query_service=query_service,
        llm_clients=llm_clients,
        default_provider=config.LLM_DEFAULT_PROVIDER,
    )


RAGServiceDep = Annotated[RAGService, Depends(get_rag_service)]
