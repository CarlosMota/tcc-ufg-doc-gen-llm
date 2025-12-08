from abc import ABC, abstractmethod

from .models import QueryInput, QueryResult


class VectorRepository(ABC):
    @abstractmethod
    def query(self, query: QueryInput) -> QueryResult:
        """Consulta documentos em um repositório vetorial."""
        raise NotImplementedError


class MessageBus(ABC):
    @abstractmethod
    def publish(self, event: str, payload: dict) -> None:
        """Publica um evento em um barramento de mensagens."""
        raise NotImplementedError

