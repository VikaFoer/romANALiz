"""Unit tests for collector queue."""
import pytest
from airbot.collector.queue import CollectorQueue


@pytest.mark.asyncio
async def test_queue_put_get():
    q = CollectorQueue()
    await q.put({"id": "1"})
    item = await q.get()
    assert item == {"id": "1"}


def test_queue_qsize():
    q = CollectorQueue()
    q.put_nowait({"a": 1})
    q.put_nowait({"b": 2})
    assert q.qsize() == 2
