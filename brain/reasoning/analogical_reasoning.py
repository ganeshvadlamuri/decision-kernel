"""Analogical reasoning - Apply solutions from similar problems."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Problem:
    """A problem and its solution."""

    description: str
    context: dict[str, Any]
    solution: list[str]
    success: bool


class AnalogicalReasoner:
    """Apply solutions from similar problems."""

    def __init__(self) -> None:
        self.problem_library: list[Problem] = []

    def store_problem(
        self, description: str, context: dict[str, Any], solution: list[str], success: bool
    ) -> None:
        """Store a solved problem."""
        self.problem_library.append(Problem(description, context, solution, success))

    def find_analogous_problem(self, current_problem: str, current_context: dict[str, Any]) -> Problem | None:
        """Find similar problem from past experience."""
        best_match = None
        best_similarity = 0.0

        for problem in self.problem_library:
            if not problem.success:
                continue

            similarity = self._calculate_similarity(
                current_problem, current_context, problem.description, problem.context
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = problem

        return best_match if best_similarity > 0.5 else None

    def adapt_solution(
        self, source_problem: Problem, target_context: dict[str, Any]
    ) -> list[str]:
        """Adapt solution from source to target context."""
        adapted_solution = []

        for action in source_problem.solution:
            # Replace context-specific terms
            adapted_action = action
            for key, value in target_context.items():
                if key in source_problem.context:
                    old_value = str(source_problem.context[key])
                    new_value = str(value)
                    adapted_action = adapted_action.replace(old_value, new_value)

            adapted_solution.append(adapted_action)

        return adapted_solution

    def solve_by_analogy(
        self, problem: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Solve problem using analogical reasoning."""
        analogous = self.find_analogous_problem(problem, context)

        if not analogous:
            return {
                "found_analogy": False,
                "solution": [],
                "confidence": 0.0,
            }

        adapted = self.adapt_solution(analogous, context)
        similarity = self._calculate_similarity(
            problem, context, analogous.description, analogous.context
        )

        return {
            "found_analogy": True,
            "source_problem": analogous.description,
            "solution": adapted,
            "confidence": similarity,
        }

    def _calculate_similarity(
        self,
        desc1: str,
        ctx1: dict[str, Any],
        desc2: str,
        ctx2: dict[str, Any],
    ) -> float:
        """Calculate similarity between two problems."""
        # Description similarity (simple word overlap)
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())
        desc_sim = len(words1 & words2) / max(len(words1 | words2), 1)

        # Context similarity (shared keys with same values)
        shared_keys = set(ctx1.keys()) & set(ctx2.keys())
        if not shared_keys:
            ctx_sim = 0.0
        else:
            matching = sum(1 for k in shared_keys if ctx1[k] == ctx2[k])
            ctx_sim = matching / len(shared_keys)

        return (desc_sim + ctx_sim) / 2
