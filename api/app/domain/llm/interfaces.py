from abc import ABC, abstractmethod

from .models import LLMRequest, LLMResponse


class LLMClient(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError
