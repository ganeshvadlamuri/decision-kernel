
from brain.planner.actions import Action


class SafetyValidator:
    """Validate plans against safety constraints"""

    def __init__(self):
        self.max_actions = 20
        self.forbidden_actions = ["harm", "damage"]

    def validate(self, plan: list[Action]) -> tuple[bool, str]:
        if len(plan) == 0:
            return False, "Empty plan"

        if len(plan) > self.max_actions:
            return False, f"Plan too long ({len(plan)} > {self.max_actions})"

        for action in plan:
            if action.action_type in self.forbidden_actions:
                return False, f"Forbidden action: {action.action_type}"

        return True, "PASS"
