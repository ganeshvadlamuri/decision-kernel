"""Interruptible execution - Pause/resume long tasks."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionState:
    """State of execution."""

    task: str
    completed_actions: list[str]
    remaining_actions: list[str]
    progress: float


class InterruptibleExecutor:
    """Pause/resume long tasks."""

    def __init__(self) -> None:
        self.saved_state: ExecutionState | None = None

    def save_state(self, task: str, completed: list[str], remaining: list[str]) -> None:
        """Save execution state."""
        total = len(completed) + len(remaining)
        progress = len(completed) / total if total > 0 else 0.0

        self.saved_state = ExecutionState(task, completed, remaining, progress)

    def resume(self) -> ExecutionState | None:
        """Resume from saved state."""
        state = self.saved_state
        self.saved_state = None
        return state

    def can_resume(self) -> bool:
        """Check if can resume."""
        return self.saved_state is not None
