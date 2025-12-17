"""Attention mechanism - Focus on relevant inputs."""

from typing import Any


class AttentionMechanism:
    """Focus on relevant inputs."""

    def compute_attention(self, inputs: list[dict[str, Any]], goal: str) -> list[tuple[dict[str, Any], float]]:
        """Compute attention weights for inputs."""
        attended = []

        for inp in inputs:
            relevance = self._compute_relevance(inp, goal)
            attended.append((inp, relevance))

        # Sort by relevance
        attended.sort(key=lambda x: x[1], reverse=True)
        return attended

    def _compute_relevance(self, inp: dict[str, Any], goal: str) -> float:
        """Compute relevance of input to goal."""
        # Simple keyword matching
        inp_str = str(inp).lower()
        goal_words = goal.lower().split()

        matches = sum(1 for word in goal_words if word in inp_str)
        return matches / len(goal_words) if goal_words else 0.0

    def focus(self, inputs: list[dict[str, Any]], goal: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Focus on top-k most relevant inputs."""
        attended = self.compute_attention(inputs, goal)
        return [inp for inp, _ in attended[:top_k]]
