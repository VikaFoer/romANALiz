"""Database interface – ready for SQLite/PostgreSQL and extensions."""
from abc import ABC, abstractmethod
from typing import Any


class Database(ABC):
    """Abstract database – connection pool, async operations."""

    @abstractmethod
    async def connect(self) -> None:
        """Create pool / open connection."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close pool / connection."""
        ...

    @abstractmethod
    async def execute(self, query: str, *args: Any, **kwargs: Any) -> Any:
        """Execute query (no result set)."""
        ...

    @abstractmethod
    async def fetch_one(self, query: str, *args: Any, **kwargs: Any) -> dict[str, Any] | None:
        """Fetch one row as dict."""
        ...

    @abstractmethod
    async def fetch_all(self, query: str, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        """Fetch all rows as list of dicts."""
        ...

    async def __aenter__(self) -> "Database":
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect()
