"""Goal conflict resolution - Handle conflicting goals."""

from typing import Any


class GoalConflictResolver:
    """'clean room' vs 'don't wake baby'."""

    def detect_conflict(self, goal1: str, goal2: str, context: dict[str, Any]) -> dict[str, Any]:
        """Detect if goals conflict."""
        conflicts = {
            ("clean_room", "don't_wake_baby"): "noise_conflict",
            ("charge_battery", "deliver_item"): "location_conflict",
            ("save_energy", "move_quickly"): "resource_conflict",
        }

        conflict_type = conflicts.get((goal1, goal2)) or conflicts.get((goal2, goal1))

        return {
            "has_conflict": conflict_type is not None,
            "conflict_type": conflict_type,
            "goals": [goal1, goal2],
        }

    def resolve(self, goal1: str, goal2: str, context: dict[str, Any]) -> dict[str, Any]:
        """Resolve goal conflict."""
        conflict = self.detect_conflict(goal1, goal2, context)

        if not conflict["has_conflict"]:
            return {"resolution": "no_conflict", "action": "proceed_both"}

        # Resolution strategies
        if conflict["conflict_type"] == "noise_conflict":
            return {
                "resolution": "postpone",
                "action": "wait_until_baby_awake",
                "priority_goal": goal2,
            }

        if conflict["conflict_type"] == "location_conflict":
            return {
                "resolution": "sequence",
                "action": "deliver_then_charge",
                "order": [goal2, goal1],
            }

        return {"resolution": "unknown", "action": "ask_human"}
