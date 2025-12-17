"""Collaboration - Work together, not just follow orders."""

from typing import Any


class CollaborationEngine:
    """Work together, not just follow orders."""

    def propose_collaboration(self, human_goal: str, robot_capabilities: list[str]) -> dict[str, Any]:
        """Propose how robot can collaborate on goal."""
        # Identify how robot can help
        contributions = [cap for cap in robot_capabilities if self._relevant_to_goal(cap, human_goal)]

        return {
            "human_goal": human_goal,
            "robot_contributions": contributions,
            "collaboration_mode": "assist" if contributions else "observe",
        }

    def _relevant_to_goal(self, capability: str, goal: str) -> bool:
        """Check if capability is relevant to goal."""
        return capability.lower() in goal.lower()
