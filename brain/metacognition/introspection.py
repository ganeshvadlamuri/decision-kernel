"""Introspection - Examine own decision process."""

from typing import Any


class Introspector:
    """Examine own decision process."""

    def analyze_decision(self, decision: dict[str, Any]) -> dict[str, Any]:
        """Analyze decision-making process."""
        factors = decision.get("factors", [])
        confidence = decision.get("confidence", 0.5)

        analysis = {
            "decision": decision.get("action"),
            "num_factors_considered": len(factors),
            "confidence": confidence,
            "decision_quality": "good" if confidence > 0.7 else "uncertain",
        }

        # Identify biases
        if len(factors) < 2:
            analysis["potential_bias"] = "insufficient_consideration"

        return analysis
