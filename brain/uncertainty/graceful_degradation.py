"""Graceful degradation - Partial success when full success impossible."""

from typing import Any


class GracefulDegradation:
    """Partial success when full success impossible."""

    def find_partial_solution(self, goal: str, failed_actions: list[str], all_actions: list[str]) -> dict[str, Any]:
        """Find partial solution when full goal cannot be achieved."""
        achievable_actions = [a for a in all_actions if a not in failed_actions]

        completion_rate = len(achievable_actions) / len(all_actions) if all_actions else 0

        return {
            "goal": goal,
            "full_success": False,
            "partial_actions": achievable_actions,
            "completion_rate": completion_rate,
            "acceptable": completion_rate >= 0.5,
        }
