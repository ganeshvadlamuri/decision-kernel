from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExecutionRecord:
    timestamp: datetime
    goal: str
    plan: list[str]
    success: bool


class Memory:
    """Store execution history"""

    def __init__(self):
        self.records: list[ExecutionRecord] = []

    def store(self, goal: str, plan: list[str], success: bool = True):
        record = ExecutionRecord(
            timestamp=datetime.now(),
            goal=goal,
            plan=plan,
            success=success
        )
        self.records.append(record)

    def get_history(self) -> list[ExecutionRecord]:
        return self.records
