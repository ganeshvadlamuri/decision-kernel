"""Working memory - Track current context across multiple commands."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class ContextItem:
    """An item in working memory."""

    key: str
    value: Any
    timestamp: datetime
    importance: float = 0.5


class WorkingMemory:
    """Track current context across multiple commands."""

    def __init__(self, capacity: int = 7, ttl_seconds: int = 300) -> None:
        self.capacity = capacity  # Miller's law: 7±2 items
        self.ttl_seconds = ttl_seconds
        self.items: dict[str, ContextItem] = {}

    def store(self, key: str, value: Any, importance: float = 0.5) -> None:
        """Store item in working memory."""
        self.items[key] = ContextItem(key, value, datetime.now(), importance)
        self._cleanup()

    def retrieve(self, key: str) -> Any | None:
        """Retrieve item from working memory."""
        self._cleanup()
        item = self.items.get(key)
        return item.value if item else None

    def has(self, key: str) -> bool:
        """Check if key exists in working memory."""
        self._cleanup()
        return key in self.items

    def get_context(self) -> dict[str, Any]:
        """Get all current context."""
        self._cleanup()
        return {k: v.value for k, v in self.items.items()}

    def clear(self) -> None:
        """Clear working memory."""
        self.items.clear()

    def _cleanup(self) -> None:
        """Remove expired and low-importance items."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.ttl_seconds)

        # Remove expired items
        self.items = {
            k: v for k, v in self.items.items() if v.timestamp > cutoff
        }

        # If over capacity, remove least important
        if len(self.items) > self.capacity:
            sorted_items = sorted(
                self.items.items(), key=lambda x: x[1].importance, reverse=True
            )
            self.items = dict(sorted_items[: self.capacity])

    def resolve_reference(self, reference: str) -> Any | None:
        """Resolve pronouns/references (it, that, here, there)."""
        reference_map = {
            "it": "last_object",
            "that": "last_object",
            "this": "last_object",
            "here": "current_location",
            "there": "last_location",
        }
        key = reference_map.get(reference.lower())
        return self.retrieve(key) if key else None
