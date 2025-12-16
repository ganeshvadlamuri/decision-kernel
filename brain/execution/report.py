"""Execution reporting structures"""

from dataclasses import dataclass, field
from enum import Enum


class ExecutionStatus(Enum):
    """Status of action execution"""

    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class ActionResult:
    """Result of a single action execution"""

    action_index: int
    status: ExecutionStatus
    message: str = ""
    duration: float = 0.0
    error: str | None = None


@dataclass
class ExecutionReport:
    """Report of plan execution"""

    success: bool
    results: list[ActionResult] = field(default_factory=list)
    total_duration: float = 0.0
    message: str = ""

    def add_result(self, result: ActionResult) -> None:
        """Add action result to report"""
        self.results.append(result)
        self.total_duration += result.duration
