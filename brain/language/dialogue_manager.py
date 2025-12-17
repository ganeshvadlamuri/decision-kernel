"""Multi-turn dialogue - Remember conversation history."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DialogueTurn:
    """A single turn in dialogue."""

    speaker: str
    utterance: str
    timestamp: datetime
    intent: str | None = None


class DialogueManager:
    """Remember conversation history."""

    def __init__(self, max_history: int = 10) -> None:
        self.history: list[DialogueTurn] = []
        self.max_history = max_history

    def add_turn(self, speaker: str, utterance: str, intent: str | None = None) -> None:
        """Add dialogue turn."""
        turn = DialogueTurn(speaker, utterance, datetime.now(), intent)
        self.history.append(turn)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_context(self) -> list[str]:
        """Get recent conversation context."""
        return [f"{t.speaker}: {t.utterance}" for t in self.history[-5:]]

    def last_user_intent(self) -> str | None:
        """Get last user intent."""
        for turn in reversed(self.history):
            if turn.speaker == "user" and turn.intent:
                return turn.intent
        return None
