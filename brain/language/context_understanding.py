"""Context understanding - Resolve references like 'it', 'here'."""

from typing import Any


class ContextUnderstanding:
    """'bring it here' (what is 'it'? where is 'here'?)."""

    def __init__(self) -> None:
        self.context: dict[str, Any] = {}

    def resolve_command(self, command: str) -> dict[str, Any]:
        """Resolve ambiguous references in command."""
        resolved = command
        references = []

        # Resolve pronouns
        if "it" in command.lower():
            obj = self.context.get("last_object", "unknown_object")
            resolved = resolved.replace("it", obj).replace("It", obj)
            references.append(("it", obj))

        if "here" in command.lower():
            loc = self.context.get("current_location", "unknown_location")
            resolved = resolved.replace("here", loc).replace("Here", loc)
            references.append(("here", loc))

        if "there" in command.lower():
            loc = self.context.get("last_location", "unknown_location")
            resolved = resolved.replace("there", loc).replace("There", loc)
            references.append(("there", loc))

        return {
            "original": command,
            "resolved": resolved,
            "references": references,
            "fully_resolved": "unknown" not in resolved,
        }

    def update_context(self, key: str, value: Any) -> None:
        """Update context."""
        self.context[key] = value
