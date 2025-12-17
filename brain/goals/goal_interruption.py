"""Goal interruption - Pause, handle emergency, resume."""

from dataclasses import dataclass
from typing import Any


@dataclass
class GoalState:
    """Saved state of a goal."""

    goal: str
    progress: dict[str, Any]
    completed_actions: list[str]


class GoalInterruptionManager:
    """Pause task, handle emergency, resume."""

    def __init__(self) -> None:
        self.paused_goals: list[GoalState] = []

    def pause_goal(self, goal: str, progress: dict[str, Any], completed: list[str]) -> None:
        """Pause current goal."""
        self.paused_goals.append(GoalState(goal, progress, completed))

    def resume_goal(self) -> GoalState | None:
        """Resume most recent paused goal."""
        return self.paused_goals.pop() if self.paused_goals else None

    def should_interrupt(self, current_priority: float, new_priority: float) -> bool:
        """Decide if new goal should interrupt current."""
        return new_priority > current_priority * 1.5
