"""Clarification questions - Ask when confused."""

from typing import Any


class ClarificationEngine:
    """Ask when confused."""

    def generate_clarification(self, ambiguity: dict[str, Any]) -> str:
        """Generate clarification question."""
        if ambiguity["type"] == "multiple_objects":
            return f"Which {ambiguity['object']}? I see {ambiguity['count']} of them."

        if ambiguity["type"] == "unknown_location":
            return f"Where is '{ambiguity['location']}'? I don't know that location."

        if ambiguity["type"] == "unclear_intent":
            return f"What do you want me to do with {ambiguity['object']}?"

        return "I don't understand. Can you clarify?"

    def should_ask(self, confidence: float, threshold: float = 0.6) -> bool:
        """Decide if clarification is needed."""
        return confidence < threshold
