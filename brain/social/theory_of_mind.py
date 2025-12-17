"""Theory of mind - Model what human knows/wants/believes."""

from typing import Any


class TheoryOfMind:
    """Model what human knows/wants/believes."""

    def __init__(self) -> None:
        self.human_model: dict[str, Any] = {
            "knows": [],
            "wants": [],
            "believes": {},
        }

    def human_knows(self, fact: str) -> bool:
        """Check if human knows fact."""
        return fact in self.human_model["knows"]

    def human_wants(self, goal: str) -> bool:
        """Check if human wants goal."""
        return goal in self.human_model["wants"]

    def should_inform(self, fact: str) -> bool:
        """Decide if human should be informed."""
        return not self.human_knows(fact)

    def update_human_knowledge(self, fact: str) -> None:
        """Update model of human knowledge."""
        if fact not in self.human_model["knows"]:
            self.human_model["knows"].append(fact)
