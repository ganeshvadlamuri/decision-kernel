"""Failure recovery - Detect, diagnose, retry differently."""


class FailureRecovery:
    """Detect failure, diagnose, retry differently."""

    def __init__(self) -> None:
        self.recovery_strategies: dict[str, list[str]] = {
            "grasp_failed": ["adjust_grip", "approach_different_angle", "use_two_hands"],
            "navigation_blocked": ["find_alternate_route", "wait_for_clearance", "ask_for_help"],
            "object_not_found": ["search_nearby", "ask_human", "check_last_known_location"],
        }

    def diagnose_failure(self, action: str, error: str) -> str:
        """Diagnose failure type."""
        failure_patterns = {
            "grasp_failed": ["slip", "drop", "miss"],
            "navigation_blocked": ["obstacle", "blocked", "stuck"],
            "object_not_found": ["not found", "missing", "absent"],
        }

        for failure_type, keywords in failure_patterns.items():
            if any(kw in error.lower() for kw in keywords):
                return failure_type

        return "unknown_failure"

    def get_recovery_strategy(self, failure_type: str) -> list[str]:
        """Get recovery strategies for failure type."""
        return self.recovery_strategies.get(failure_type, ["retry", "ask_for_help"])

    def should_retry(self, attempts: int, max_attempts: int = 3) -> bool:
        """Decide if should retry."""
        return attempts < max_attempts
