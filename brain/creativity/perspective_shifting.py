"""Perspective shifting - view problems from multiple angles."""

from typing import Any


class PerspectiveShifting:
    """Solve problems by viewing from different perspectives."""

    def __init__(self) -> None:
        self.perspectives = self._build_perspectives()

    def solve_from_multiple_views(
        self, problem: dict[str, Any]
    ) -> dict[str, Any]:
        """Solve problem from multiple perspectives."""
        solutions = []

        for perspective_name, perspective_func in self.perspectives.items():
            solution = perspective_func(problem)
            solutions.append(
                {
                    "perspective": perspective_name,
                    "solution": solution,
                    "novelty": solution.get("novelty", 0.5),
                    "practicality": solution.get("practicality", 0.5),
                }
            )

        best_solution = self.synthesize_best(solutions)

        return {
            "problem": problem,
            "perspectives_considered": len(solutions),
            "all_solutions": solutions,
            "best_solution": best_solution,
        }

    def view_as_human(self, problem: dict[str, Any]) -> dict[str, Any]:
        """View problem from human perspective."""
        return {
            "approach": "empathy_driven",
            "solution": "Consider human comfort and preferences",
            "actions": [
                "Ask human for preferences",
                "Prioritize safety and comfort",
                "Communicate clearly",
            ],
            "novelty": 0.3,
            "practicality": 0.9,
        }

    def view_as_engineer(self, problem: dict[str, Any]) -> dict[str, Any]:
        """View problem from engineering perspective."""
        return {
            "approach": "optimization_driven",
            "solution": "Optimize for efficiency and reliability",
            "actions": [
                "Analyze constraints",
                "Calculate optimal path",
                "Minimize resource usage",
            ],
            "novelty": 0.5,
            "practicality": 0.8,
        }

    def view_as_child(self, problem: dict[str, Any]) -> dict[str, Any]:
        """View problem from child's perspective (naive, creative)."""
        return {
            "approach": "curiosity_driven",
            "solution": "Try unconventional approaches",
            "actions": [
                "Experiment with different methods",
                "Ignore conventional constraints",
                "Play with possibilities",
            ],
            "novelty": 0.9,
            "practicality": 0.4,
        }

    def view_as_expert(self, problem: dict[str, Any]) -> dict[str, Any]:
        """View problem from expert perspective."""
        return {
            "approach": "knowledge_driven",
            "solution": "Apply domain expertise and best practices",
            "actions": [
                "Use proven techniques",
                "Apply domain knowledge",
                "Follow best practices",
            ],
            "novelty": 0.4,
            "practicality": 0.9,
        }

    def view_as_artist(self, problem: dict[str, Any]) -> dict[str, Any]:
        """View problem from artistic perspective."""
        return {
            "approach": "aesthetic_driven",
            "solution": "Create elegant and beautiful solution",
            "actions": [
                "Consider visual appeal",
                "Optimize for elegance",
                "Balance form and function",
            ],
            "novelty": 0.7,
            "practicality": 0.5,
        }

    def synthesize_best(
        self, solutions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Synthesize best solution from multiple perspectives."""
        # Score each solution
        scored = []
        for sol in solutions:
            score = (sol["novelty"] * 0.3) + (sol["practicality"] * 0.7)
            scored.append({"solution": sol, "score": score})

        # Get best
        best = max(scored, key=lambda x: x["score"])

        # Combine insights from multiple perspectives
        combined_actions = []
        for sol in solutions:
            if sol["practicality"] > 0.6:
                combined_actions.extend(sol["solution"]["actions"])

        return {
            "primary_perspective": best["solution"]["perspective"],
            "approach": best["solution"]["solution"]["approach"],
            "combined_actions": list(set(combined_actions)),
            "overall_score": best["score"],
            "reasoning": f"Best balance of novelty and practicality from {best['solution']['perspective']} view",
        }

    def _build_perspectives(self) -> dict[str, Any]:
        """Build perspective functions."""
        return {
            "human": self.view_as_human,
            "engineer": self.view_as_engineer,
            "child": self.view_as_child,
            "expert": self.view_as_expert,
            "artist": self.view_as_artist,
        }
