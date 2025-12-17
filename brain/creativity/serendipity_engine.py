"""Serendipity engine - notice unexpected opportunities."""

from typing import Any


class SerendipityEngine:
    """Detect and act on unexpected opportunities."""

    def __init__(self) -> None:
        self.opportunity_patterns = self._build_opportunity_patterns()

    def detect_opportunities(
        self, current_state: dict[str, Any]
    ) -> dict[str, Any]:
        """Detect opportunities in current state."""
        opportunities = []

        objects = current_state.get("objects", [])
        current_location = current_state.get("location", "unknown")
        current_goal = current_state.get("current_goal", "")

        for obj in objects:
            opportunity = self.is_opportunity(obj, current_location, current_goal)
            if opportunity:
                opportunities.append(opportunity)

        return {
            "opportunities_found": len(opportunities),
            "opportunities": opportunities,
            "should_act": len(opportunities) > 0,
        }

    def is_opportunity(
        self, obj: dict[str, Any], location: str, current_goal: str
    ) -> dict[str, Any] | None:
        """Check if object represents an opportunity."""
        obj_name = obj.get("name", "")
        obj_state = obj.get("state", "")

        for pattern in self.opportunity_patterns:
            if self._matches_pattern(pattern, obj_name, obj_state, location):
                return self.create_optional_goal(pattern, obj, location)

        return None

    def _matches_pattern(
        self, pattern: dict[str, Any], obj_name: str, obj_state: str, location: str
    ) -> bool:
        """Check if object matches opportunity pattern."""
        # Check object type
        if pattern.get("object_type") and pattern["object_type"] not in obj_name:
            return False

        # Check state
        if pattern.get("required_state") and obj_state != pattern["required_state"]:
            return False

        # Check location
        if pattern.get("location") and location != pattern["location"]:
            return False

        return True

    def create_optional_goal(
        self, pattern: dict[str, Any], obj: dict[str, Any], location: str
    ) -> dict[str, Any]:
        """Create optional goal from opportunity."""
        return {
            "type": "optional_goal",
            "goal": pattern["goal"],
            "description": pattern["description"],
            "object": obj["name"],
            "location": location,
            "priority": pattern.get("priority", "low"),
            "estimated_time": pattern.get("estimated_time", 30),
            "benefit": pattern.get("benefit", "medium"),
        }

    def should_pursue(
        self, opportunity: dict[str, Any], current_context: dict[str, Any]
    ) -> dict[str, Any]:
        """Decide if opportunity should be pursued."""
        priority = opportunity.get("priority", "low")
        estimated_time = opportunity.get("estimated_time", 30)
        available_time = current_context.get("available_time", 0)
        current_priority = current_context.get("current_priority", "high")

        # Don't interrupt high priority tasks
        if current_priority == "high" and priority != "high":
            return {
                "pursue": False,
                "reason": "Current task has higher priority",
            }

        # Check if we have time
        if estimated_time > available_time:
            return {
                "pursue": False,
                "reason": "Insufficient time available",
            }

        # Pursue if conditions met
        return {
            "pursue": True,
            "reason": f"Good opportunity with {priority} priority",
        }

    def _build_opportunity_patterns(self) -> list[dict[str, Any]]:
        """Build patterns for recognizing opportunities."""
        return [
            {
                "object_type": "dish",
                "required_state": "dirty",
                "location": "kitchen",
                "goal": "clean_dishes",
                "description": "Noticed dirty dishes while in kitchen",
                "priority": "low",
                "estimated_time": 60,
                "benefit": "medium",
            },
            {
                "object_type": "trash",
                "required_state": "full",
                "location": "any",
                "goal": "empty_trash",
                "description": "Noticed full trash bin",
                "priority": "medium",
                "estimated_time": 30,
                "benefit": "high",
            },
            {
                "object_type": "light",
                "required_state": "on",
                "location": "any",
                "goal": "turn_off_light",
                "description": "Noticed light on in empty room",
                "priority": "low",
                "estimated_time": 10,
                "benefit": "low",
            },
            {
                "object_type": "door",
                "required_state": "open",
                "location": "any",
                "goal": "close_door",
                "description": "Noticed door left open",
                "priority": "medium",
                "estimated_time": 15,
                "benefit": "medium",
            },
            {
                "object_type": "plant",
                "required_state": "dry",
                "location": "any",
                "goal": "water_plant",
                "description": "Noticed plant needs watering",
                "priority": "low",
                "estimated_time": 45,
                "benefit": "medium",
            },
            {
                "object_type": "item",
                "required_state": "misplaced",
                "location": "any",
                "goal": "organize_item",
                "description": "Noticed item out of place",
                "priority": "low",
                "estimated_time": 20,
                "benefit": "low",
            },
        ]
