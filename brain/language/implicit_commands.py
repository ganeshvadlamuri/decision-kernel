"""Implicit commands - Infer intent from statements."""

from typing import Any


class ImplicitCommandParser:
    """'I'm thirsty' → bring water."""

    def __init__(self) -> None:
        self.intent_patterns: dict[str, str] = {
            "i'm thirsty": "bring_water",
            "i'm hungry": "bring_food",
            "it's dark": "turn_on_lights",
            "it's cold": "increase_temperature",
            "it's hot": "decrease_temperature",
            "i'm tired": "prepare_bed",
            "i can't see": "turn_on_lights",
            "it's noisy": "reduce_noise",
        }

    def parse(self, statement: str) -> dict[str, Any]:
        """Parse implicit command."""
        statement_lower = statement.lower()

        for pattern, intent in self.intent_patterns.items():
            if pattern in statement_lower:
                return {
                    "statement": statement,
                    "is_implicit_command": True,
                    "intent": intent,
                    "confidence": 0.85,
                }

        return {
            "statement": statement,
            "is_implicit_command": False,
            "intent": None,
            "confidence": 0.0,
        }

    def add_pattern(self, pattern: str, intent: str) -> None:
        """Add new implicit command pattern."""
        self.intent_patterns[pattern.lower()] = intent
