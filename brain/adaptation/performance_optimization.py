"""Performance optimization - Get faster at repeated tasks."""

from typing import Any


class PerformanceOptimizer:
    """Get faster at repeated tasks."""

    def __init__(self) -> None:
        self.task_times: dict[str, list[float]] = {}
        self.optimizations: dict[str, list[str]] = {}

    def record_execution(self, task: str, duration: float) -> None:
        """Record task execution time."""
        if task not in self.task_times:
            self.task_times[task] = []
        self.task_times[task].append(duration)

    def identify_optimization(self, task: str) -> dict[str, Any]:
        """Identify optimization opportunities."""
        if task not in self.task_times or len(self.task_times[task]) < 3:
            return {"task": task, "optimizations": [], "potential_speedup": 0.0}

        times = self.task_times[task]
        avg_time = sum(times) / len(times)
        best_time = min(times)

        potential_speedup = (avg_time - best_time) / avg_time if avg_time > 0 else 0

        optimizations = []
        if potential_speedup > 0.2:
            optimizations.append("cache_intermediate_results")
        if len(times) > 10:
            optimizations.append("learn_shortcuts")

        return {
            "task": task,
            "avg_time": avg_time,
            "best_time": best_time,
            "potential_speedup": potential_speedup,
            "optimizations": optimizations,
        }
