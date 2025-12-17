"""Goal abandonment - Know when to give up."""

from typing import Any


class GoalAbandonmentDecider:
    """Know when to give up."""

    def should_abandon(
        self, goal: str, attempts: int, time_spent: float, max_attempts: int = 3, max_time: float = 300
    ) -> dict[str, Any]:
        """Decide if goal should be abandoned."""
        reasons = []

        if attempts >= max_attempts:
            reasons.append(f"exceeded_max_attempts ({attempts}/{max_attempts})")

        if time_spent >= max_time:
            reasons.append(f"exceeded_max_time ({time_spent:.0f}s/{max_time}s)")

        should_abandon = len(reasons) > 0

        return {
            "goal": goal,
            "should_abandon": should_abandon,
            "reasons": reasons,
            "attempts": attempts,
            "time_spent": time_spent,
        }
