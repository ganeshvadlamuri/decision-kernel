"""Online learning - Update models during execution."""


class OnlineLearner:
    """Update models during execution."""

    def __init__(self, learning_rate: float = 0.1) -> None:
        self.learning_rate = learning_rate
        self.action_success_rates: dict[str, float] = {}
        self.action_counts: dict[str, int] = {}

    def update_from_experience(self, action: str, success: bool) -> None:
        """Update model from execution result."""
        if action not in self.action_success_rates:
            self.action_success_rates[action] = 0.5
            self.action_counts[action] = 0

        # Incremental average
        current_rate = self.action_success_rates[action]
        new_observation = 1.0 if success else 0.0

        self.action_success_rates[action] = (
            current_rate + self.learning_rate * (new_observation - current_rate)
        )
        self.action_counts[action] += 1

    def get_success_rate(self, action: str) -> float:
        """Get learned success rate for action."""
        return self.action_success_rates.get(action, 0.5)
