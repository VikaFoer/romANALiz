"""Webhook output – optional, enabled via settings."""
from typing import Any
import httpx
from airbot.config import get_settings


class WebhookOutput:
    """POST events to webhook URL."""

    def __init__(self) -> None:
        s = get_settings()
        self._url = s.webhook_url
        self._enabled = s.webhook_enabled and bool(s.webhook_url.strip())

    async def send(self, payload: dict[str, Any]) -> None:
        if not self._enabled or not self._url:
            return
        async with httpx.AsyncClient() as client:
            await client.post(self._url, json=payload, timeout=10.0)
