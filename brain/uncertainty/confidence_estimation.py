"""Confidence estimation - Know certainty level."""

from typing import Any


class ConfidenceEstimator:
    """'I'm 60% sure this will work'."""

    def estimate_action_confidence(self, action: str, context: dict[str, Any]) -> float:
        """Estimate confidence in action success."""
        base_confidence = 0.7

        # Adjust based on past experience
        if "past_success_rate" in context:
            base_confidence = context["past_success_rate"]

        # Reduce if missing information
        if "missing_info" in context:
            base_confidence *= (1 - len(context["missing_info"]) * 0.1)

        return max(0.0, min(1.0, base_confidence))

    def should_proceed(self, confidence: float, threshold: float = 0.6) -> bool:
        """Decide if confidence is sufficient to proceed."""
        return confidence >= threshold
