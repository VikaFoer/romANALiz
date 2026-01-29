"""Output router – fan-out to Kafka and/or Webhook."""
from typing import Any
from airbot.output.kafka_output import KafkaOutput
from airbot.output.webhook_output import WebhookOutput


class OutputRouter:
    """Route events to all enabled outputs."""

    def __init__(self) -> None:
        self._kafka = KafkaOutput()
        self._webhook = WebhookOutput()

    async def start(self) -> None:
        await self._kafka.start()

    async def stop(self) -> None:
        await self._kafka.stop()

    async def emit(self, event_id: str, payload: dict[str, Any]) -> None:
        await self._kafka.send(event_id, payload)
        await self._webhook.send(payload)
