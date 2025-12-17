"""Probabilistic planning - Plan under uncertainty."""

import random
from typing import Any


class ProbabilisticPlanner:
    """Plan under uncertainty."""

    def plan_with_uncertainty(self, goal: str, action_success_probs: dict[str, float]) -> dict[str, Any]:
        """Generate plan considering action success probabilities."""
        actions = list(action_success_probs.keys())
        plan_success_prob = 1.0

        for action in actions:
            plan_success_prob *= action_success_probs[action]

        return {
            "goal": goal,
            "plan": actions,
            "success_probability": plan_success_prob,
            "needs_contingency": plan_success_prob < 0.7,
        }

    def monte_carlo_simulation(self, plan: list[str], probs: dict[str, float], runs: int = 100) -> float:
        """Simulate plan execution multiple times."""
        successes = 0
        for _ in range(runs):
            if all(random.random() < probs[action] for action in plan):
                successes += 1
        return successes / runs
