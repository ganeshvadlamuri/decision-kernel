"""Strategy switching - Try different approaches when stuck."""

from typing import Any


class StrategySwitcher:
    """Try different approaches when stuck."""

    def __init__(self) -> None:
        self.strategies: dict[str, list[str]] = {
            "navigate": ["direct_path", "avoid_obstacles", "follow_wall", "ask_directions"],
            "grasp": ["top_grasp", "side_grasp", "pinch_grasp", "scoop"],
            "search": ["systematic_scan", "random_search", "ask_human", "check_common_places"],
        }
        self.current_strategy: dict[str, int] = {}

    def get_next_strategy(self, task: str) -> str | None:
        """Get next strategy to try."""
        if task not in self.strategies:
            return None

        if task not in self.current_strategy:
            self.current_strategy[task] = 0
        else:
            self.current_strategy[task] += 1

        idx = self.current_strategy[task]
        strategies = self.strategies[task]

        if idx >= len(strategies):
            return None  # Exhausted all strategies

        return strategies[idx]

    def reset_strategy(self, task: str) -> None:
        """Reset to first strategy."""
        self.current_strategy[task] = 0
