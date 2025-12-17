"""Environment adaptation - Adjust to new homes/layouts."""

from typing import Any


class EnvironmentAdapter:
    """Adjust to new homes/layouts."""

    def __init__(self) -> None:
        self.environment_model: dict[str, Any] = {}

    def learn_environment(self, observations: list[dict[str, Any]]) -> None:
        """Learn environment from observations."""
        for obs in observations:
            location = obs.get("location")
            if location:
                if location not in self.environment_model:
                    self.environment_model[location] = {"objects": [], "layout": {}}

                if "object" in obs:
                    self.environment_model[location]["objects"].append(obs["object"])

    def adapt_behavior(self, new_environment: str) -> dict[str, Any]:
        """Adapt behavior to new environment."""
        if new_environment not in self.environment_model:
            return {
                "environment": new_environment,
                "adaptations": ["explore_mode", "cautious_navigation"],
                "confidence": 0.3,
            }

        return {
            "environment": new_environment,
            "adaptations": ["use_learned_layout", "normal_speed"],
            "confidence": 0.8,
        }
