"""Information gathering - Know what you don't know."""

from typing import Any


class InformationGatherer:
    """Know what you don't know, ask/explore."""

    def identify_unknowns(self, required_info: list[str], known_info: dict[str, Any]) -> list[str]:
        """Identify missing information."""
        return [info for info in required_info if info not in known_info]

    def generate_query(self, unknown: str) -> str:
        """Generate query to gather information."""
        query_templates = {
            "object_location": f"Where is the {unknown}?",
            "object_state": f"What is the state of {unknown}?",
            "human_preference": f"Do you prefer {unknown}?",
        }
        return query_templates.get(unknown, f"What is {unknown}?")

    def should_explore(self, confidence: float, threshold: float = 0.5) -> bool:
        """Decide if exploration is needed."""
        return confidence < threshold
