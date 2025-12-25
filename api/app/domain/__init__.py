"""Camada de domínio: contratos e entidades."""

from .interfaces.message_bus import MessageBus
from .search.repositories import VectorRepository

__all__ = ["MessageBus", "VectorRepository"]
