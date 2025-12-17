"""Episodic memory - Remember specific past events."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Episode:
    """A specific past event."""

    timestamp: datetime
    action: str
    context: dict[str, Any]
    outcome: str
    success: bool
    duration_seconds: float


class EpisodicMemory:
    """Remember specific past events ('last time I did X, Y happened')."""

    def __init__(self, max_episodes: int = 1000) -> None:
        self.episodes: list[Episode] = []
        self.max_episodes = max_episodes

    def record(
        self,
        action: str,
        context: dict[str, Any],
        outcome: str,
        success: bool,
        duration_seconds: float,
    ) -> Episode:
        """Record a new episode."""
        episode = Episode(
            timestamp=datetime.now(),
            action=action,
            context=context,
            outcome=outcome,
            success=success,
            duration_seconds=duration_seconds,
        )
        self.episodes.append(episode)

        # Keep only recent episodes
        if len(self.episodes) > self.max_episodes:
            self.episodes = self.episodes[-self.max_episodes :]

        return episode

    def recall(self, action: str, context_filter: dict[str, Any] | None = None) -> list[Episode]:
        """Recall past episodes matching action and context."""
        matches = [e for e in self.episodes if e.action == action]

        if context_filter:
            matches = [
                e
                for e in matches
                if all(e.context.get(k) == v for k, v in context_filter.items())
            ]

        return sorted(matches, key=lambda e: e.timestamp, reverse=True)

    def last_time(self, action: str) -> Episode | None:
        """Get the last time this action was performed."""
        matches = [e for e in self.episodes if e.action == action]
        return matches[-1] if matches else None

    def success_rate(self, action: str) -> float:
        """Calculate success rate for an action."""
        matches = [e for e in self.episodes if e.action == action]
        if not matches:
            return 0.0
        return sum(1 for e in matches if e.success) / len(matches)

    def average_duration(self, action: str) -> float:
        """Calculate average duration for an action."""
        matches = [e for e in self.episodes if e.action == action]
        if not matches:
            return 0.0
        return sum(e.duration_seconds for e in matches) / len(matches)
