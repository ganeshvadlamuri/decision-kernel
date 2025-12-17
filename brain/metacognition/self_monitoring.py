"""Self-monitoring - Know when confused/stuck."""

from typing import Any


class SelfMonitor:
    """Know when you're confused/stuck."""

    def check_state(self, context: dict[str, Any]) -> dict[str, Any]:
        """Check current cognitive state."""
        is_confused = context.get("confidence", 1.0) < 0.4
        is_stuck = context.get("progress", 1.0) < 0.1 and context.get("time_elapsed", 0) > 30

        state = "normal"
        if is_confused:
            state = "confused"
        elif is_stuck:
            state = "stuck"

        return {
            "state": state,
            "is_confused": is_confused,
            "is_stuck": is_stuck,
            "needs_help": is_confused or is_stuck,
        }
