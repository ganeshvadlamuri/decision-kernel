"""Common sense reasoning - Know implicit rules."""

from dataclasses import dataclass
from typing import Any


@dataclass
class CommonSenseRule:
    """An implicit rule about the world."""

    rule: str
    context: dict[str, Any]
    priority: float


class CommonSenseReasoner:
    """Know implicit rules ('don't vacuum while human sleeps')."""

    def __init__(self) -> None:
        self.rules: list[CommonSenseRule] = []
        self._init_common_rules()

    def _init_common_rules(self) -> None:
        """Initialize common sense rules."""
        rules: list[tuple[str, dict[str, Any], float]] = [
            ("don't_make_noise_when_human_sleeping", {"time": "night", "human_state": "sleeping"}, 0.95),
            ("don't_block_doorways", {"location": "doorway"}, 0.90),
            ("don't_touch_hot_objects", {"object_temp": "hot"}, 0.95),
            ("don't_spill_liquids", {"holding": "liquid"}, 0.85),
            ("don't_wake_babies", {"human_type": "baby", "baby_state": "sleeping"}, 0.98),
            ("clean_spills_immediately", {"floor_state": "wet"}, 0.80),
            ("turn_off_lights_when_leaving", {"room_state": "empty"}, 0.60),
            ("close_fridge_door", {"fridge_state": "open"}, 0.90),
            ("don't_interrupt_conversations", {"humans_talking": True}, 0.75),
            ("ask_before_throwing_away", {"object_ownership": "unknown"}, 0.85),
        ]

        for rule, context, priority in rules:
            self.rules.append(CommonSenseRule(rule, context, priority))

    def check_action(self, action: str, context: dict[str, Any]) -> dict[str, Any]:
        """Check if action violates common sense."""
        violations = []

        for rule in self.rules:
            if self._matches_context(rule.context, context):
                if self._violates_rule(action, rule.rule):
                    violations.append({
                        "rule": rule.rule,
                        "priority": rule.priority,
                        "suggestion": self._get_suggestion(rule.rule),
                    })

        return {
            "action": action,
            "violations": violations,
            "safe": len(violations) == 0,
            "highest_priority_violation": max((v["priority"] for v in violations), default=0.0) if violations else 0.0,
        }

    def should_avoid(self, action: str, context: dict[str, Any]) -> bool:
        """Check if action should be avoided."""
        result = self.check_action(action, context)
        priority: float = result["highest_priority_violation"]
        return priority > 0.7

    def add_rule(self, rule: str, context: dict[str, Any], priority: float) -> None:
        """Add new common sense rule."""
        self.rules.append(CommonSenseRule(rule, context, priority))

    def _matches_context(self, rule_context: dict[str, Any], actual_context: dict[str, Any]) -> bool:
        """Check if actual context matches rule context."""
        for key, value in rule_context.items():
            if key not in actual_context or actual_context[key] != value:
                return False
        return True

    def _violates_rule(self, action: str, rule: str) -> bool:
        """Check if action violates rule."""
        violation_map = {
            "don't_make_noise_when_human_sleeping": ["vacuum", "play_music", "bang"],
            "don't_block_doorways": ["stop", "wait", "park"],
            "don't_touch_hot_objects": ["grasp", "touch", "pick_up"],
            "don't_wake_babies": ["make_noise", "vacuum", "slam_door"],
            "close_fridge_door": [],  # Omission, not action
        }

        for keyword in violation_map.get(rule, []):
            if keyword in action.lower():
                return True
        return False

    def _get_suggestion(self, rule: str) -> str:
        """Get suggestion for violated rule."""
        suggestions = {
            "don't_make_noise_when_human_sleeping": "Wait until human wakes up",
            "don't_block_doorways": "Move to side of room",
            "don't_touch_hot_objects": "Wait for object to cool down",
            "don't_wake_babies": "Postpone noisy tasks",
            "close_fridge_door": "Close the fridge door",
        }
        return suggestions.get(rule, "Reconsider this action")
