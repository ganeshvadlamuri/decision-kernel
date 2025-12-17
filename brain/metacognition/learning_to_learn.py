"""Learning to learn - Improve learning efficiency."""

from typing import Any


class MetaLearner:
    """Improve learning efficiency."""

    def __init__(self) -> None:
        self.learning_history: list[dict[str, Any]] = []

    def record_learning_episode(self, task: str, time_to_learn: float, final_performance: float) -> None:
        """Record learning episode."""
        self.learning_history.append({
            "task": task,
            "time_to_learn": time_to_learn,
            "final_performance": final_performance,
        })

    def optimize_learning_strategy(self) -> dict[str, Any]:
        """Identify how to learn faster."""
        if len(self.learning_history) < 3:
            return {"strategy": "default", "improvement": 0.0}

        avg_time = sum(e["time_to_learn"] for e in self.learning_history) / len(self.learning_history)
        recent_time = self.learning_history[-1]["time_to_learn"]

        improvement = (avg_time - recent_time) / avg_time if avg_time > 0 else 0

        strategy = "increase_practice" if improvement < 0 else "current_approach_working"

        return {
            "strategy": strategy,
            "improvement": improvement,
            "learning_rate_trend": "improving" if improvement > 0 else "declining",
        }
