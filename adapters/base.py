"""Base adapter contract"""

from typing import Protocol

from brain.execution.report import ExecutionReport
from brain.planner.actions import Action
from brain.world.state import WorldState


class Adapter(Protocol):
    """Adapter contract for hardware/simulation integration"""

    def sense(self) -> WorldState:
        """
        Sense environment and return current world state

        Returns:
            WorldState with current environment representation
        """
        ...

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Execute action plan

        Args:
            plan: List of actions to execute

        Returns:
            ExecutionReport with results
        """
        ...

    def capabilities(self) -> dict:
        """
        Report adapter capabilities

        Returns:
            Dictionary describing supported actions and features
        """
        ...
