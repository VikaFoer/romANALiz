"""Worker pool – process queue items with detectors + scoring + output."""
import asyncio
from typing import Any
from airbot.config import get_settings
from airbot.collector.queue import CollectorQueue
from airbot.detectors import get_detectors
from airbot.detectors.base import BaseDetector, DetectorResult
from airbot.scoring import ScoringEngine
from airbot.output import OutputRouter


class WorkerPool:
    """Pool of workers: get from queue -> run detectors -> score -> emit."""

    def __init__(
        self,
        queue: CollectorQueue,
        output: OutputRouter,
        pool_size: int | None = None,
    ) -> None:
        self._queue = queue
        self._output = output
        self._pool_size = pool_size or get_settings().worker_pool_size
        self._scoring = ScoringEngine()
        self._detector_instances: list[BaseDetector] = [
            cls() for cls in get_detectors()
        ]
        self._running = False
        self._tasks: list[asyncio.Task[None]] = []

    async def _process_one(self, item: dict[str, Any]) -> None:
        results: list[DetectorResult] = []
        for det in self._detector_instances:
            out = await det.run(item)
            if isinstance(out, list):
                results.extend(out)
            else:
                results.append(out)
        if not results:
            return
        score = self._scoring.aggregate(results)
        event_id = results[0].event_id
        payload = {
            "event_id": event_id,
            "score": score,
            "detector_results": [
                {"detector": r.detector_name, "score": r.score}
                for r in results
            ],
            "payload": item,
        }
        await self._output.emit(event_id, payload)

    async def _worker(self) -> None:
        while self._running:
            try:
                item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._process_one(item)
            except asyncio.TimeoutError:
                continue
            except Exception:
                # log and continue
                continue

    async def start(self) -> None:
        self._running = True
        await self._output.start()
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self._pool_size)]

    async def stop(self) -> None:
        self._running = False
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        await self._output.stop()
