"""Kafka output – optional, enabled via settings."""
from typing import Any
from airbot.config import get_settings


class KafkaOutput:
    """Send events to Kafka topic."""

    def __init__(self) -> None:
        self._producer = None
        self._enabled = get_settings().kafka_enabled
        self._topic = get_settings().kafka_topic
        self._servers = get_settings().kafka_bootstrap_servers

    async def start(self) -> None:
        if not self._enabled:
            return
        try:
            from aiokafka import AIOKafkaProducer
            self._producer = AIOKafkaProducer(bootstrap_servers=self._servers)
            await self._producer.start()
        except Exception:
            self._enabled = False

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, key: str | None, value: dict[str, Any]) -> None:
        if not self._enabled or not self._producer:
            return
        import json
        await self._producer.send_and_wait(
            self._topic,
            value=json.dumps(value).encode(),
            key=key.encode() if key else None,
        )
