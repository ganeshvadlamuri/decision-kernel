"""Goal prioritization - Urgent vs important."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Goal:
    """A goal with priority attributes."""

    description: str
    urgency: float  # 0-1
    importance: float  # 0-1
    deadline: float | None = None  # seconds until deadline


class GoalPrioritizer:
    """Urgent vs important."""

    def prioritize(self, goals: list[Goal]) -> list[Goal]:
        """Prioritize goals using Eisenhower matrix."""
        scored_goals = []
        for goal in goals:
            score = self._calculate_priority_score(goal)
            scored_goals.append((goal, score))

        scored_goals.sort(key=lambda x: x[1], reverse=True)
        return [g for g, _ in scored_goals]

    def _calculate_priority_score(self, goal: Goal) -> float:
        """Calculate priority score."""
        # Eisenhower: urgent + important
        base_score = (goal.urgency * 0.6) + (goal.importance * 0.4)

        # Deadline pressure
        if goal.deadline and goal.deadline < 300:  # < 5 minutes
            base_score *= 1.5

        return min(base_score, 1.0)
