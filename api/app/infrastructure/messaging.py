import logging
from typing import Optional

import aio_pika

from .. import config
from ..domain.repositories import MessageBus


class LoggingMessageBus(MessageBus):
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def publish(self, event: str, payload: dict) -> None:
        self.logger.info("event=%s payload=%s", event, payload)


class RabbitMQMessageBus(MessageBus):
    """Publicação simplificada em fila RabbitMQ (fire-and-forget)."""

    def __init__(self, url: Optional[str] = None, queue: str = "events") -> None:
        self.url = url or config.MESSAGE_BROKER_URL
        if not self.url:
            raise ValueError("MESSAGE_BROKER_URL não configurada.")
        self.queue = queue

    def publish(self, event: str, payload: dict) -> None:
        # Uso síncrono mínimo apenas para demonstração; produção deve usar loop/async.
        import asyncio

        asyncio.run(self._publish_async(event, payload))

    async def _publish_async(self, event: str, payload: dict) -> None:
        connection = await aio_pika.connect_robust(self.url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue, durable=True)
            body = f"{event}|{payload}".encode("utf-8")
            await channel.default_exchange.publish(
                aio_pika.Message(body=body),
                routing_key=queue.name,
            )

