"""Explanation generation - Explain decisions."""

from typing import Any


class ExplanationGenerator:
    """'I did X because Y'."""

    def explain_action(self, action: str, reasoning: dict[str, Any]) -> str:
        """Generate explanation for action."""
        goal = reasoning.get("goal", "unknown goal")
        reason = reasoning.get("reason", "it seemed appropriate")

        return f"I {action} because {reason} to achieve {goal}"

    def explain_failure(self, action: str, error: str) -> str:
        """Explain why action failed."""
        return f"I couldn't {action} because {error}"

    def explain_decision(self, chosen: str, alternatives: list[str], criteria: str) -> str:
        """Explain why option was chosen."""
        return f"I chose {chosen} over {', '.join(alternatives)} because {criteria}"
