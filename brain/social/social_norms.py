"""Social norms - Learn cultural rules."""

from typing import Any


class SocialNormsLearner:
    """Learn cultural rules (personal space, politeness)."""

    def __init__(self) -> None:
        self.norms: dict[str, dict[str, Any]] = {
            "personal_space": {"min_distance": 1.0, "priority": 0.9},
            "eye_contact": {"duration": 2.0, "priority": 0.6},
            "interruption": {"allowed": False, "priority": 0.8},
            "volume": {"max_level": 0.7, "priority": 0.7},
        }

    def check_norm_violation(self, action: str, context: dict[str, Any]) -> dict[str, Any]:
        """Check if action violates social norms."""
        violations = []

        if "distance_to_human" in context and context["distance_to_human"] < self.norms["personal_space"]["min_distance"]:
            violations.append("personal_space_violation")

        return {
            "action": action,
            "violations": violations,
            "acceptable": len(violations) == 0,
        }
