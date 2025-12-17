"""Tool improvisation - use objects in unexpected ways."""

from typing import Any


class ToolImprovisation:
    """Find alternative tools when standard tools unavailable."""

    def __init__(self) -> None:
        self.function_mappings = self._build_function_mappings()

    def find_alternative_tool(
        self, needed_function: str, available_objects: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Find object that can perform needed function."""
        candidates = []

        for obj in available_objects:
            if self.can_perform_function(obj, needed_function):
                method = self.how_to_use(obj, needed_function)
                confidence = self.calculate_confidence(obj, needed_function)
                candidates.append(
                    {
                        "object": obj["name"],
                        "method": method,
                        "confidence": confidence,
                        "improvised": obj["name"]
                        not in self.function_mappings.get(needed_function, {}).get(
                            "standard_tools", []
                        ),
                    }
                )

        if not candidates:
            return {
                "success": False,
                "message": f"No alternative found for {needed_function}",
            }

        best = max(candidates, key=lambda x: x["confidence"])
        return {"success": True, "alternative": best}

    def can_perform_function(
        self, obj: dict[str, Any], function: str
    ) -> bool:
        """Check if object can perform function."""
        obj_properties = set(obj.get("properties", []))
        required_properties = set(
            self.function_mappings.get(function, {}).get("required_properties", [])
        )

        return bool(required_properties & obj_properties)

    def how_to_use(self, obj: dict[str, Any], function: str) -> str:
        """Generate instructions for using object."""
        obj_name = obj["name"]
        function_data = self.function_mappings.get(function, {})

        if obj_name in function_data.get("standard_tools", []):
            return str(function_data.get("standard_method", "Use normally"))

        # Generate improvised method
        obj_properties = obj.get("properties", [])

        if function == "cut":
            if "sharp" in obj_properties:
                return f"Use sharp edge of {obj_name} to cut"
            if "rigid" in obj_properties:
                return f"Use {obj_name} to tear along fold"

        if function == "measure":
            if "known_size" in obj_properties:
                return f"Use {obj_name} as reference (known size)"

        if function == "reach":
            if "long" in obj_properties:
                return f"Use {obj_name} to extend reach"

        return f"Improvise with {obj_name}"

    def calculate_confidence(self, obj: dict[str, Any], function: str) -> float:
        """Calculate confidence in improvised tool."""
        obj_name = obj["name"]
        function_data = self.function_mappings.get(function, {})

        # Standard tool = high confidence
        if obj_name in function_data.get("standard_tools", []):
            return 0.95

        # Check property match
        obj_properties = set(obj.get("properties", []))
        required = set(function_data.get("required_properties", []))
        match_ratio = len(obj_properties & required) / max(len(required), 1)

        # Improvised tool = lower confidence
        return 0.4 + (match_ratio * 0.4)

    def _build_function_mappings(self) -> dict[str, dict[str, Any]]:
        """Build mappings of functions to tools and properties."""
        return {
            "cut": {
                "standard_tools": ["scissors", "knife", "blade"],
                "required_properties": ["sharp", "rigid"],
                "standard_method": "Use cutting edge",
                "alternatives": ["card_edge", "string", "tear_by_hand"],
            },
            "measure": {
                "standard_tools": ["ruler", "tape_measure"],
                "required_properties": ["known_size", "rigid"],
                "standard_method": "Align and read measurement",
                "alternatives": ["hand_span", "foot_length", "reference_object"],
            },
            "reach": {
                "standard_tools": ["stick", "pole", "grabber"],
                "required_properties": ["long", "rigid"],
                "standard_method": "Extend to target",
                "alternatives": ["broom", "umbrella", "hanger"],
            },
            "contain": {
                "standard_tools": ["box", "container", "bag"],
                "required_properties": ["hollow", "enclosed"],
                "standard_method": "Place inside",
                "alternatives": ["cup", "drawer", "pocket"],
            },
            "fasten": {
                "standard_tools": ["tape", "glue", "clip"],
                "required_properties": ["adhesive", "binding"],
                "standard_method": "Apply and press",
                "alternatives": ["rubber_band", "string", "paperclip"],
            },
            "illuminate": {
                "standard_tools": ["flashlight", "lamp"],
                "required_properties": ["light_source"],
                "standard_method": "Turn on and point",
                "alternatives": ["phone_screen", "match", "reflective_surface"],
            },
        }
