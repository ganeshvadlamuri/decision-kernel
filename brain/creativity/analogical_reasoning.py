"""Analogical reasoning - solve new problems by adapting past solutions."""

from typing import Any


class AnalogicalReasoning:
    """Find similar past problems and adapt solutions to new contexts."""

    def __init__(self) -> None:
        self.case_library: list[dict[str, Any]] = []
        self._seed_cases()

    def solve_novel_problem(self, problem: dict[str, Any]) -> dict[str, Any]:
        """Solve new problem using analogical reasoning."""
        similar_case = self.find_most_similar(problem)

        if not similar_case:
            return {"success": False, "reason": "no_similar_case"}

        adapted = self.adapt_solution(similar_case, problem)
        confidence = self.calculate_similarity(problem, similar_case)

        return {
            "success": True,
            "solution": adapted,
            "source_case": similar_case["name"],
            "confidence": confidence,
            "reasoning": f"Adapted from '{similar_case['name']}'",
        }

    def find_most_similar(self, problem: dict[str, Any]) -> dict[str, Any] | None:
        """Find most similar case from library."""
        best_match = None
        best_score = 0.0

        for case in self.case_library:
            score = self.calculate_similarity(problem, case)
            if score > best_score:
                best_score = score
                best_match = case

        return best_match if best_score > 0.3 else None

    def calculate_similarity(
        self, problem: dict[str, Any], case: dict[str, Any]
    ) -> float:
        """Calculate similarity between problem and case."""
        score = 0.0
        weights = {"goal": 0.4, "context": 0.3, "constraints": 0.3}

        if problem.get("goal") == case.get("goal"):
            score += weights["goal"]

        problem_context = set(problem.get("context", []))
        case_context = set(case.get("context", []))
        if problem_context & case_context:
            overlap = len(problem_context & case_context) / max(
                len(problem_context), len(case_context), 1
            )
            score += weights["context"] * overlap

        problem_constraints = set(problem.get("constraints", []))
        case_constraints = set(case.get("constraints", []))
        if problem_constraints & case_constraints:
            overlap = len(problem_constraints & case_constraints) / max(
                len(problem_constraints), len(case_constraints), 1
            )
            score += weights["constraints"] * overlap

        return score

    def adapt_solution(
        self, source_case: dict[str, Any], target_problem: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Adapt source solution to target problem."""
        source_solution = source_case.get("solution", [])
        adapted = []

        for action in source_solution:
            adapted_action = action.copy()

            # Substitute target-specific parameters
            if "target" in target_problem:
                adapted_action["target"] = target_problem["target"]
            if "location" in target_problem:
                adapted_action["location"] = target_problem["location"]

            adapted.append(adapted_action)

        return adapted

    def add_case(self, case: dict[str, Any]) -> None:
        """Add new case to library for future reasoning."""
        self.case_library.append(case)

    def _seed_cases(self) -> None:
        """Seed library with common problem-solution pairs."""
        self.case_library = [
            {
                "name": "bring_object",
                "goal": "transport",
                "context": ["object", "location"],
                "constraints": ["graspable"],
                "solution": [
                    {"action": "navigate_to", "target": "object_location"},
                    {"action": "grasp", "target": "object"},
                    {"action": "navigate_to", "target": "destination"},
                    {"action": "release", "target": "object"},
                ],
            },
            {
                "name": "clean_area",
                "goal": "clean",
                "context": ["area", "dirty"],
                "constraints": ["accessible"],
                "solution": [
                    {"action": "navigate_to", "target": "area"},
                    {"action": "clean", "target": "area"},
                    {"action": "verify_clean", "target": "area"},
                ],
            },
            {
                "name": "open_container",
                "goal": "access",
                "context": ["container", "closed"],
                "constraints": ["openable"],
                "solution": [
                    {"action": "navigate_to", "target": "container"},
                    {"action": "grasp", "target": "lid"},
                    {"action": "twist", "target": "lid"},
                    {"action": "release", "target": "lid"},
                ],
            },
        ]
