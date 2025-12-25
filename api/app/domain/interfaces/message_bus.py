from abc import ABC, abstractmethod


class MessageBus(ABC):
    @abstractmethod
    def publish(self, event: str, payload: dict) -> None:
        """Publica um evento em um barramento de mensagens."""
        raise NotImplementedError
