"""Interfaces (contratos) da camada de domínio."""

from .message_bus import MessageBus
from .vector_repository import VectorRepository

__all__ = ["MessageBus", "VectorRepository"]
