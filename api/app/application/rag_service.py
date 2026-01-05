from typing import Dict, Iterable, Optional

from ..domain.llm import LLMClient, LLMRequest
from ..domain.search.models import DocumentHit, QueryInput, RAGInput, RAGResponse
from ..domain.search.service import QueryService


class PromptBuilder:
    def build(self, query: QueryInput, hits: Iterable[DocumentHit]) -> str:
        raise NotImplementedError


class DefaultPromptBuilder(PromptBuilder):
    def build(self, query: QueryInput, hits: Iterable[DocumentHit]) -> str:
        context_chunks = []
        for idx, hit in enumerate(hits, start=1):
            context_chunks.append(
                f"[{idx}] score={hit.score:.3f} id={hit.id}\n{hit.text}"
            )
        context = "\n\n".join(context_chunks) if context_chunks else "Sem contexto."
        return (
            "Use o contexto abaixo para responder a pergunta.\n\n"
            f"Pergunta: {query.text}\n\n"
            f"Contexto:\n{context}\n\n"
            "Resposta:"
        )


class RAGService:
    def __init__(
        self,
        query_service: QueryService,
        llm_clients: Dict[str, LLMClient],
        prompt_builder: Optional[PromptBuilder] = None,
        default_provider: Optional[str] = None,
    ) -> None:
        self.query_service = query_service
        self.llm_clients = llm_clients
        self.prompt_builder = prompt_builder or DefaultPromptBuilder()
        self.default_provider = default_provider

    def answer(self, rag_input: RAGInput) -> RAGResponse:
        result = self.query_service.search(rag_input)
        prompt = self.prompt_builder.build(rag_input, result.hits)

        provider = rag_input.provider or self.default_provider
        if not provider and self.llm_clients:
            provider = next(iter(self.llm_clients.keys()))
        client = self.llm_clients.get(provider) if provider else None
        if not client:
            raise ValueError(f"Provedor LLM desconhecido: {provider}")

        request = LLMRequest(
            prompt=prompt,
            model=rag_input.model,
            temperature=rag_input.temperature,
            max_tokens=rag_input.max_tokens,
        )
        response = client.generate(request)
        return RAGResponse(query=rag_input.text, answer=response.text, hits=result.hits)
