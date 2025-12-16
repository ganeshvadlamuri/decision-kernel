from typing import Any

from brain.intent.parser import IntentParser
from brain.memory.memory import Memory
from brain.planner.actions import Action
from brain.planner.planner import Planner
from brain.safety.rules import SafetyValidator
from brain.skills.registry import SkillRegistry
from brain.world.state import WorldState


class RobotBrainKernel:
    """Core orchestration layer for robot decision-making"""

    def __init__(
        self,
        skill_registry: SkillRegistry | None = None,
        adapter: Any | None = None,
    ):
        self.intent_parser = IntentParser()
        self.planner = Planner(skill_registry=skill_registry)
        self.safety = SafetyValidator()
        self.memory = Memory()
        self.adapter = adapter

    def process(self, human_input: str, world_state: WorldState) -> list[Action]:
        """
        Main processing pipeline:
        Intent → Planning → Safety → Memory → Actions
        """

        goal = self.intent_parser.parse(human_input)
        plan = self.planner.plan(goal, world_state)

        is_safe, reason = self.safety.validate(plan)
        if not is_safe:
            raise ValueError(f"Safety check failed: {reason}")

        # Check adapter capabilities if adapter provided
        if self.adapter is not None:
            self._check_capabilities(plan)

        plan_str = [str(action) for action in plan]
        self.memory.store(goal=str(goal), plan=plan_str)

        return plan

    def _check_capabilities(self, plan: list[Action]) -> None:
        """Check if adapter supports all actions in plan"""
        if self.adapter is None or not hasattr(self.adapter, "capabilities"):
            return

        caps = self.adapter.capabilities()
        supported = caps.get("supported_actions", [])

        for action in plan:
            if action.action_type not in supported:
                raise ValueError(
                    f"Adapter does not support action: {action.action_type}. "
                    f"Supported actions: {supported}"
                )
