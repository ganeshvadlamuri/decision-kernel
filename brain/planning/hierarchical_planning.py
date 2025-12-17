"""Hierarchical planning - High-level strategy + low-level tactics."""

from typing import Any


class HierarchicalPlanner:
    """High-level strategy + low-level tactics."""

    def __init__(self) -> None:
        self.high_level_plans: dict[str, list[str]] = {
            "clean_house": ["clean_kitchen", "clean_bedroom", "clean_bathroom"],
            "prepare_meal": ["get_ingredients", "cook", "serve"],
        }
        self.low_level_plans: dict[str, list[str]] = {
            "clean_kitchen": ["wipe_counters", "wash_dishes", "sweep_floor"],
            "get_ingredients": ["open_fridge", "grasp_item", "place_on_counter"],
        }

    def plan(self, goal: str) -> dict[str, Any]:
        """Generate hierarchical plan."""
        if goal in self.high_level_plans:
            high_level = self.high_level_plans[goal]
            low_level = []

            for subtask in high_level:
                if subtask in self.low_level_plans:
                    low_level.extend(self.low_level_plans[subtask])
                else:
                    low_level.append(subtask)

            return {
                "goal": goal,
                "high_level": high_level,
                "low_level": low_level,
                "total_actions": len(low_level),
            }

        return {"goal": goal, "high_level": [goal], "low_level": [goal], "total_actions": 1}
