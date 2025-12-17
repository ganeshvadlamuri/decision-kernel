"""Ambiguity resolution - Handle multiple interpretations."""

from typing import Any


class AmbiguityResolver:
    """'get the cup' (which cup?)."""

    def __init__(self) -> None:
        self.world_state: dict[str, list[dict[str, Any]]] = {}

    def detect_ambiguity(self, command: str) -> dict[str, Any]:
        """Detect ambiguous references."""
        words = command.lower().split()
        ambiguities = []

        for word in words:
            if word in self.world_state and len(self.world_state[word]) > 1:
                ambiguities.append({
                    "object": word,
                    "count": len(self.world_state[word]),
                    "options": self.world_state[word],
                })

        return {
            "command": command,
            "is_ambiguous": len(ambiguities) > 0,
            "ambiguities": ambiguities,
        }

    def resolve_with_context(self, obj_type: str, context: dict[str, Any]) -> dict[str, Any] | None:
        """Resolve using context (nearest, most recent, etc)."""
        if obj_type not in self.world_state:
            return None

        candidates = self.world_state[obj_type]
        if len(candidates) == 1:
            return candidates[0]

        # Prefer nearest
        if "robot_location" in context:
            candidates = sorted(candidates, key=lambda x: x.get("distance", 999))

        return candidates[0] if candidates else None

    def add_object(self, obj_type: str, properties: dict[str, Any]) -> None:
        """Add object to world state."""
        if obj_type not in self.world_state:
            self.world_state[obj_type] = []
        self.world_state[obj_type].append(properties)
