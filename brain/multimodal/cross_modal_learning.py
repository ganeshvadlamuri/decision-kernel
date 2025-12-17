"""Cross-modal learning - Associate across modalities."""

from typing import Any


class CrossModalLearner:
    """'red' (vision) = 'apple' (word) = 'crunchy' (sound)."""

    def __init__(self) -> None:
        self.associations: dict[str, dict[str, Any]] = {}

    def associate(self, concept: str, modality: str, value: Any) -> None:
        """Associate value with concept in modality."""
        if concept not in self.associations:
            self.associations[concept] = {}
        self.associations[concept][modality] = value

    def query(self, concept: str, target_modality: str) -> Any | None:
        """Query concept in target modality."""
        if concept in self.associations:
            return self.associations[concept].get(target_modality)
        return None

    def infer_concept(self, modality: str, value: Any) -> list[str]:
        """Infer concepts from modality value."""
        matches = []
        for concept, modalities in self.associations.items():
            if modalities.get(modality) == value:
                matches.append(concept)
        return matches
