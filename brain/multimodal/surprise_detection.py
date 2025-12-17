"""Surprise detection - Notice unexpected events."""

from typing import Any


class SurpriseDetector:
    """Notice unexpected events."""

    def __init__(self) -> None:
        self.expectations: dict[str, Any] = {}

    def set_expectation(self, key: str, expected_value: Any) -> None:
        """Set expectation for key."""
        self.expectations[key] = expected_value

    def detect_surprise(self, observation: dict[str, Any]) -> dict[str, Any]:
        """Detect if observation is surprising."""
        surprises = []

        for key, observed_value in observation.items():
            if key in self.expectations:
                expected_value = self.expectations[key]
                if observed_value != expected_value:
                    surprises.append({
                        "key": key,
                        "expected": expected_value,
                        "observed": observed_value,
                    })

        return {
            "is_surprising": len(surprises) > 0,
            "surprises": surprises,
            "surprise_level": len(surprises) / max(len(self.expectations), 1),
        }
