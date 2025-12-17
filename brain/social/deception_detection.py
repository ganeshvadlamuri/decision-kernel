"""Deception detection - Recognize joking/lying."""

from typing import Any


class DeceptionDetector:
    """Recognize when human is joking/lying."""

    def detect(self, statement: str, context: dict[str, Any]) -> dict[str, Any]:
        """Detect if statement is deceptive or joking."""
        # Simple heuristics
        is_joke = any(marker in statement.lower() for marker in ["haha", "lol", "just kidding"])

        # Contradiction with known facts
        is_lie = context.get("contradicts_known_facts", False)

        return {
            "statement": statement,
            "is_joke": is_joke,
            "is_lie": is_lie,
            "should_take_literally": not (is_joke or is_lie),
        }
