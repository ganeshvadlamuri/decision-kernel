"""Meta-strategy selection - choose the right thinking approach for each problem."""

from collections.abc import Callable
from typing import Any


class MetaStrategy:
    """Select appropriate reasoning strategy based on problem type."""

    def __init__(self) -> None:
        self.strategies: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}
        self.problem_classifiers: list[dict[str, Any]] = self._build_classifiers()

    def select_strategy(self, problem: dict[str, Any]) -> dict[str, Any]:
        """Select best strategy for problem type."""
        problem_class = self.classify_problem(problem)
        strategy_name = self._get_strategy_for_class(problem_class)

        return {
            "problem_class": problem_class,
            "selected_strategy": strategy_name,
            "reasoning": self._explain_selection(problem_class, strategy_name),
        }

    def classify_problem(self, problem: dict[str, Any]) -> str:
        """Classify problem into category."""
        problem_text = problem.get("description", "").lower()
        problem_context = problem.get("context", {})

        # Check each classifier
        for classifier in self.problem_classifiers:
            if self._matches_classifier(classifier, problem_text, problem_context):
                return str(classifier["class"])

        return "novel"  # Default for unrecognized problems

    def _matches_classifier(
        self, classifier: dict[str, Any], text: str, context: dict[str, Any]
    ) -> bool:
        """Check if problem matches classifier."""
        # Check keywords
        keywords = classifier.get("keywords", [])
        if keywords and any(kw in text for kw in keywords):
            return True

        # Check context conditions
        conditions = classifier.get("context_conditions", [])
        for condition in conditions:
            key = condition["key"]
            if key in context and context[key] == condition["value"]:
                return True

        return False

    def _get_strategy_for_class(self, problem_class: str) -> str:
        """Get strategy name for problem class."""
        strategy_map = {
            "routine": "cached_solution",
            "novel": "analogical_reasoning",
            "impossible": "constraint_relaxation",
            "ambiguous": "information_gathering",
            "complex": "hierarchical_decomposition",
            "uncertain": "probabilistic_reasoning",
            "creative": "conceptual_blending",
        }
        return strategy_map.get(problem_class, "general_planning")

    def _explain_selection(self, problem_class: str, strategy: str) -> str:
        """Explain why strategy was selected."""
        explanations = {
            "routine": "Problem is familiar, using cached solution for efficiency",
            "novel": "Problem is new, using analogical reasoning from similar cases",
            "impossible": "Problem seems impossible, trying constraint relaxation",
            "ambiguous": "Problem is unclear, gathering more information first",
            "complex": "Problem is complex, breaking into smaller sub-problems",
            "uncertain": "Problem has uncertainty, using probabilistic reasoning",
            "creative": "Problem needs creativity, using conceptual blending",
        }
        return explanations.get(
            problem_class, "Using general planning for unclassified problem"
        )

    def _build_classifiers(self) -> list[dict[str, Any]]:
        """Build problem classifiers."""
        return [
            {
                "class": "routine",
                "keywords": ["bring", "fetch", "get", "clean", "simple"],
                "context_conditions": [{"key": "seen_before", "value": True}],
            },
            {
                "class": "novel",
                "keywords": ["new", "never", "first time", "unfamiliar"],
                "context_conditions": [{"key": "seen_before", "value": False}],
            },
            {
                "class": "impossible",
                "keywords": [
                    "impossible",
                    "can't",
                    "unable",
                    "mars",
                    "moon",
                    "teleport",
                ],
                "context_conditions": [{"key": "feasible", "value": False}],
            },
            {
                "class": "ambiguous",
                "keywords": ["unclear", "maybe", "not sure", "which", "what"],
                "context_conditions": [{"key": "clarity", "value": "low"}],
            },
            {
                "class": "complex",
                "keywords": [
                    "multiple",
                    "many",
                    "several",
                    "complex",
                    "complicated",
                ],
                "context_conditions": [{"key": "num_steps", "value": 10}],
            },
            {
                "class": "uncertain",
                "keywords": ["might", "possibly", "uncertain", "risky", "chance"],
                "context_conditions": [{"key": "uncertainty", "value": "high"}],
            },
            {
                "class": "creative",
                "keywords": [
                    "creative",
                    "innovative",
                    "unusual",
                    "unique",
                    "original",
                ],
                "context_conditions": [{"key": "requires_creativity", "value": True}],
            },
        ]

    def execute_strategy(
        self, strategy_name: str, problem: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute selected strategy on problem."""
        if strategy_name in self.strategies:
            return self.strategies[strategy_name](problem)

        # Default execution
        return {
            "success": True,
            "strategy": strategy_name,
            "result": f"Would execute {strategy_name} on problem",
        }

    def register_strategy(self, name: str, strategy_func: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        """Register custom strategy function."""
        self.strategies[name] = strategy_func
