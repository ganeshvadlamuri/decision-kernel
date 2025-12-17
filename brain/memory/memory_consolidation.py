"""Memory consolidation - Compress old memories, keep important ones."""

from datetime import datetime, timedelta
from typing import Any

from .episodic_memory import Episode, EpisodicMemory


class ConsolidatedMemory:
    """Compressed representation of multiple episodes."""

    def __init__(self, action: str, episodes: list[Episode]) -> None:
        self.action = action
        self.count = len(episodes)
        self.success_rate = sum(1 for e in episodes if e.success) / len(episodes)
        self.avg_duration = sum(e.duration_seconds for e in episodes) / len(episodes)
        self.common_context = self._extract_common_context(episodes)
        self.typical_outcome = self._most_common_outcome(episodes)

    def _extract_common_context(self, episodes: list[Episode]) -> dict[str, Any]:
        """Extract context features common to all episodes."""
        if not episodes:
            return {}

        common = {}
        first_context = episodes[0].context

        for key in first_context:
            values = [e.context.get(key) for e in episodes if key in e.context]
            if len(set(values)) == 1:  # All same value
                common[key] = values[0]

        return common

    def _most_common_outcome(self, episodes: list[Episode]) -> str:
        """Find most common outcome."""
        outcomes = [e.outcome for e in episodes]
        return max(set(outcomes), key=outcomes.count)


class MemoryConsolidator:
    """Compress old memories, keep important ones."""

    def __init__(self, consolidation_threshold_days: int = 7) -> None:
        self.consolidation_threshold_days = consolidation_threshold_days
        self.consolidated: list[ConsolidatedMemory] = []

    def consolidate(self, episodic_memory: EpisodicMemory) -> dict[str, Any]:
        """Consolidate old episodic memories."""
        cutoff = datetime.now() - timedelta(days=self.consolidation_threshold_days)
        old_episodes = [e for e in episodic_memory.episodes if e.timestamp < cutoff]
        recent_episodes = [e for e in episodic_memory.episodes if e.timestamp >= cutoff]

        # Group old episodes by action
        action_groups: dict[str, list[Episode]] = {}
        for episode in old_episodes:
            if episode.action not in action_groups:
                action_groups[episode.action] = []
            action_groups[episode.action].append(episode)

        # Consolidate each group
        consolidated_count = 0
        for action, episodes in action_groups.items():
            if len(episodes) >= 3:  # Only consolidate if multiple episodes
                self.consolidated.append(ConsolidatedMemory(action, episodes))
                consolidated_count += len(episodes)

        # Keep only recent episodes in episodic memory
        episodic_memory.episodes = recent_episodes

        return {
            "consolidated_memories": len(self.consolidated),
            "episodes_compressed": consolidated_count,
            "episodes_remaining": len(recent_episodes),
            "compression_ratio": (
                consolidated_count / len(self.consolidated) if self.consolidated else 0
            ),
        }

    def recall_consolidated(self, action: str) -> ConsolidatedMemory | None:
        """Recall consolidated memory for action."""
        matches = [c for c in self.consolidated if c.action == action]
        return matches[-1] if matches else None
