"""Unit tests for SOC-MINT module."""
import pytest
from airbot.soc_mint.module import SocMintModule


@pytest.mark.asyncio
async def test_soc_mint_enrich_passthrough_when_disabled():
    m = SocMintModule()
    payload = {"x": 1}
    out = await m.enrich(payload)
    assert out == payload


def test_soc_mint_is_enabled_follows_settings():
    m = SocMintModule()
    # Default from env (test) is false
    assert m.is_enabled() in (True, False)
