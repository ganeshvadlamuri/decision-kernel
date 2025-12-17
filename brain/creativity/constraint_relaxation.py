"""Constraint relaxation - find creative solutions by relaxing constraints."""

from typing import Any


class ConstraintRelaxation:
    """Relax constraints when stuck to find creative workarounds."""

    def __init__(self) -> None:
        self.constraint_priorities = {
            "time": 1,
            "cost": 2,
            "quality": 3,
            "safety": 10,  # Never relax safety
        }

    def plan_with_relaxation(
        self, goal: dict[str, Any], constraints: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Try planning with progressive constraint relaxation."""
        # Try with all constraints
        plan = self._attempt_plan(goal, constraints)
        if plan:
            return {
                "success": True,
                "plan": plan,
                "relaxed_constraints": [],
                "message": "Solved with all constraints",
            }

        # Try relaxing constraints by priority
        sorted_constraints = sorted(
            constraints, key=lambda c: self.constraint_priorities.get(c["type"], 5)
        )

        for i, constraint in enumerate(sorted_constraints):
            if self.constraint_priorities.get(constraint["type"], 5) >= 10:
                continue  # Never relax critical constraints

            relaxed = [c for j, c in enumerate(sorted_constraints) if j != i]
            plan = self._attempt_plan(goal, relaxed)

            if plan:
                return {
                    "success": True,
                    "plan": plan,
                    "relaxed_constraints": [constraint],
                    "message": f"Relaxed {constraint['type']}: {constraint['value']}",
                }

        return {
            "success": False,
            "plan": [],
            "relaxed_constraints": [],
            "message": "No solution found even with relaxation",
        }

    def _attempt_plan(
        self, goal: dict[str, Any], constraints: list[dict[str, Any]]
    ) -> list[dict[str, Any]] | None:
        """Attempt to create plan with given constraints."""
        # Check if goal is achievable with constraints
        if not self._is_feasible(goal, constraints):
            return None

        # Generate simple plan
        plan = []
        goal_type = goal.get("type")

        if goal_type == "transport":
            plan = [
                {"action": "navigate_to", "target": goal.get("source")},
                {"action": "grasp", "target": goal.get("object")},
                {"action": "navigate_to", "target": goal.get("destination")},
                {"action": "release", "target": goal.get("object")},
            ]
        elif goal_type == "clean":
            plan = [
                {"action": "navigate_to", "target": goal.get("location")},
                {"action": "clean", "target": goal.get("location")},
            ]

        # Verify plan meets constraints
        if self._verify_plan(plan, constraints):
            return plan

        return None

    def _is_feasible(
        self, goal: dict[str, Any], constraints: list[dict[str, Any]]
    ) -> bool:
        """Check if goal is theoretically achievable."""
        # Basic feasibility checks
        for constraint in constraints:
            if constraint["type"] == "impossible":
                return False
            if constraint["type"] == "requires" and not constraint.get("available"):
                return False
        return True

    def _verify_plan(
        self, plan: list[dict[str, Any]], constraints: list[dict[str, Any]]
    ) -> bool:
        """Verify plan satisfies constraints."""
        plan_time = len(plan) * 10  # Estimate 10s per action
        plan_cost = len(plan) * 1.0  # Estimate cost

        for constraint in constraints:
            if constraint["type"] == "time" and plan_time > constraint["value"]:
                return False
            if constraint["type"] == "cost" and plan_cost > constraint["value"]:
                return False
            if constraint["type"] == "max_actions" and len(plan) > constraint["value"]:
                return False

        return True

    def suggest_alternatives(
        self, failed_goal: dict[str, Any], constraints: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Suggest alternative approaches when relaxation fails."""
        alternatives = []

        # Suggest breaking into smaller goals
        alternatives.append(
            {
                "approach": "decompose",
                "description": "Break goal into smaller sub-goals",
                "feasibility": 0.7,
            }
        )

        # Suggest using different tools
        alternatives.append(
            {
                "approach": "alternative_tools",
                "description": "Use different tools or methods",
                "feasibility": 0.6,
            }
        )

        # Suggest asking for help
        alternatives.append(
            {
                "approach": "request_assistance",
                "description": "Request human assistance",
                "feasibility": 0.9,
            }
        )

        return alternatives
