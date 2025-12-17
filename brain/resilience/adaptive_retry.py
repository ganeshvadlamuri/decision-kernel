"""Adaptive retry that changes strategy on each attempt."""

from typing import Any


class AdaptiveRetry:
    """Try different strategies on each retry attempt."""

    def __init__(self) -> None:
        self.strategy_history: dict[str, dict[str, list[bool]]] = {}

    def execute_with_strategies(
        self, action_name: str, strategies: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Execute action with different strategies until one succeeds."""
        results = []

        for i, strategy in enumerate(strategies):
            try:
                # In real implementation, strategy would modify action execution
                result = self._execute_with_strategy(action_name, strategy)
                self._record_success(action_name, strategy["name"])
                return {
                    "success": True,
                    "result": result,
                    "strategy_used": strategy["name"],
                    "attempts": i + 1,
                }
            except Exception as e:
                self._record_failure(action_name, strategy["name"])
                results.append(
                    {"strategy": strategy["name"], "error": str(e), "attempt": i + 1}
                )

        return {
            "success": False,
            "error": "All strategies exhausted",
            "attempts": len(strategies),
            "strategy_results": results,
        }

    def get_best_strategy(self, action_name: str) -> str | None:
        """Get historically best strategy for action."""
        if action_name not in self.strategy_history:
            return None

        # Calculate success rate for each strategy
        best_strategy = None
        best_rate = 0.0

        for strategy, results in self.strategy_history[action_name].items():
            if results:
                success_rate = sum(results) / len(results)
                if success_rate > best_rate:
                    best_rate = success_rate
                    best_strategy = strategy

        return best_strategy

    def _execute_with_strategy(
        self, action_name: str, strategy: dict[str, Any]
    ) -> Any:
        """Execute action with specific strategy."""
        # Placeholder - real implementation would apply strategy
        return {"action": action_name, "strategy": strategy}

    def _record_success(self, action_name: str, strategy_name: str) -> None:
        """Record successful strategy execution."""
        if action_name not in self.strategy_history:
            self.strategy_history[action_name] = {}
        if strategy_name not in self.strategy_history[action_name]:
            self.strategy_history[action_name][strategy_name] = []
        self.strategy_history[action_name][strategy_name].append(True)

    def _record_failure(self, action_name: str, strategy_name: str) -> None:
        """Record failed strategy execution."""
        if action_name not in self.strategy_history:
            self.strategy_history[action_name] = {}
        if strategy_name not in self.strategy_history[action_name]:
            self.strategy_history[action_name][strategy_name] = []
        self.strategy_history[action_name][strategy_name].append(False)
