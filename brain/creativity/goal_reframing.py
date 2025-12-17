"""Goal reframing - reinterpret impossible goals to find achievable alternatives."""

from typing import Any


class GoalReframing:
    """Reframe impossible goals by understanding underlying needs."""

    def __init__(self) -> None:
        self.need_mappings = self._build_need_mappings()

    def reframe_impossible_goal(self, goal: dict[str, Any]) -> dict[str, Any]:
        """Reframe impossible goal into achievable alternatives."""
        if self._is_achievable(goal):
            return {
                "success": True,
                "reframed": False,
                "original_goal": goal,
                "message": "Goal is already achievable",
            }

        underlying_need = self.extract_underlying_need(goal)
        alternatives = self.find_alternative_goals(underlying_need, goal)

        if alternatives:
            return {
                "success": True,
                "reframed": True,
                "original_goal": goal,
                "underlying_need": underlying_need,
                "alternatives": alternatives,
                "message": f"Reframed to address need: {underlying_need}",
            }

        return {
            "success": False,
            "reframed": False,
            "original_goal": goal,
            "message": "Could not find achievable alternative",
        }

    def extract_underlying_need(self, goal: dict[str, Any]) -> str:
        """Extract the real need behind the goal."""
        goal_text = goal.get("description", "").lower()

        # Pattern matching for common needs
        if "water" in goal_text or "drink" in goal_text or "thirsty" in goal_text:
            return "hydration"
        if "food" in goal_text or "eat" in goal_text or "hungry" in goal_text:
            return "nutrition"
        if "warm" in goal_text or "cold" in goal_text or "temperature" in goal_text:
            return "thermal_comfort"
        if "light" in goal_text or "dark" in goal_text or "see" in goal_text:
            return "visibility"
        if "clean" in goal_text or "dirty" in goal_text or "mess" in goal_text:
            return "cleanliness"
        if "reach" in goal_text or "get" in goal_text or "access" in goal_text:
            return "accessibility"

        return "unknown"

    def find_alternative_goals(
        self, need: str, original_goal: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Find achievable goals that satisfy the same need."""
        alternatives = []

        need_data = self.need_mappings.get(need, {})
        for alt in need_data.get("alternatives", []):
            alternatives.append(
                {
                    "goal": alt["goal"],
                    "description": alt["description"],
                    "feasibility": alt["feasibility"],
                    "satisfies_need": need,
                }
            )

        return sorted(alternatives, key=lambda x: x["feasibility"], reverse=True)

    def _is_achievable(self, goal: dict[str, Any]) -> bool:
        """Check if goal is achievable."""
        impossible_keywords = [
            "mars",
            "moon",
            "impossible",
            "teleport",
            "time travel",
            "fly without",
        ]

        goal_text = goal.get("description", "").lower()
        return not any(keyword in goal_text for keyword in impossible_keywords)

    def _build_need_mappings(self) -> dict[str, Any]:
        """Build mappings of needs to alternative goals."""
        return {
            "hydration": {
                "description": "Need for water/liquid",
                "alternatives": [
                    {
                        "goal": "bring_water_from_kitchen",
                        "description": "Get water from kitchen tap",
                        "feasibility": 0.95,
                    },
                    {
                        "goal": "bring_bottled_water",
                        "description": "Get bottled water from fridge",
                        "feasibility": 0.90,
                    },
                    {
                        "goal": "bring_juice",
                        "description": "Get alternative beverage",
                        "feasibility": 0.85,
                    },
                ],
            },
            "nutrition": {
                "description": "Need for food",
                "alternatives": [
                    {
                        "goal": "bring_snack",
                        "description": "Get quick snack from pantry",
                        "feasibility": 0.90,
                    },
                    {
                        "goal": "prepare_simple_meal",
                        "description": "Make simple meal",
                        "feasibility": 0.70,
                    },
                    {
                        "goal": "order_delivery",
                        "description": "Order food delivery",
                        "feasibility": 0.60,
                    },
                ],
            },
            "thermal_comfort": {
                "description": "Need for temperature regulation",
                "alternatives": [
                    {
                        "goal": "adjust_thermostat",
                        "description": "Change room temperature",
                        "feasibility": 0.95,
                    },
                    {
                        "goal": "bring_blanket",
                        "description": "Get blanket for warmth",
                        "feasibility": 0.90,
                    },
                    {
                        "goal": "open_window",
                        "description": "Ventilate room",
                        "feasibility": 0.85,
                    },
                ],
            },
            "visibility": {
                "description": "Need for light/vision",
                "alternatives": [
                    {
                        "goal": "turn_on_lights",
                        "description": "Activate room lighting",
                        "feasibility": 0.95,
                    },
                    {
                        "goal": "open_curtains",
                        "description": "Let in natural light",
                        "feasibility": 0.90,
                    },
                    {
                        "goal": "bring_flashlight",
                        "description": "Get portable light source",
                        "feasibility": 0.85,
                    },
                ],
            },
            "cleanliness": {
                "description": "Need for clean environment",
                "alternatives": [
                    {
                        "goal": "clean_specific_area",
                        "description": "Clean targeted area",
                        "feasibility": 0.90,
                    },
                    {
                        "goal": "remove_trash",
                        "description": "Take out garbage",
                        "feasibility": 0.85,
                    },
                    {
                        "goal": "organize_items",
                        "description": "Tidy up items",
                        "feasibility": 0.80,
                    },
                ],
            },
            "accessibility": {
                "description": "Need to reach/access something",
                "alternatives": [
                    {
                        "goal": "use_tool_to_reach",
                        "description": "Use stick/grabber to reach",
                        "feasibility": 0.85,
                    },
                    {
                        "goal": "move_obstacle",
                        "description": "Remove blocking object",
                        "feasibility": 0.80,
                    },
                    {
                        "goal": "request_human_help",
                        "description": "Ask human for assistance",
                        "feasibility": 0.95,
                    },
                ],
            },
        }
