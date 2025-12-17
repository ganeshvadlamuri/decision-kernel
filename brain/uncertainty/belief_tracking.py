"""Belief tracking - Maintain probability distributions."""

from typing import Any


class BeliefTracker:
    """Maintain probability distributions."""

    def __init__(self) -> None:
        self.beliefs: dict[str, dict[str, float]] = {}

    def update_belief(self, variable: str, value: str, probability: float) -> None:
        """Update belief about variable."""
        if variable not in self.beliefs:
            self.beliefs[variable] = {}
        self.beliefs[variable][value] = probability

    def get_belief(self, variable: str) -> dict[str, float]:
        """Get belief distribution for variable."""
        return self.beliefs.get(variable, {})

    def most_likely(self, variable: str) -> tuple[str, float] | None:
        """Get most likely value for variable."""
        beliefs = self.get_belief(variable)
        if not beliefs:
            return None
        best = max(beliefs.items(), key=lambda x: x[1])
        return best
