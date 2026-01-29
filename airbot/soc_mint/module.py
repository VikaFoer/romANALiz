"""SOC-MINT module – optional, enabled via settings; hook for NLP models."""
from typing import Any
from airbot.config import get_settings


class SocMintModule:
    """SOC-MINT: optional enrichment / NLP hook."""

    def __init__(self) -> None:
        self._enabled = get_settings().soc_mint_enabled
        self._nlp_path = get_settings().nlp_model_path

    def is_enabled(self) -> bool:
        return self._enabled

    async def enrich(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Enrich payload (e.g. NLP); return updated payload."""
        if not self._enabled:
            return payload
        # Placeholder: load NLP model from self._nlp_path and run
        return payload
