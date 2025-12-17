"""Forgetting mechanism - Delete outdated/wrong information."""

import math
from datetime import datetime
from typing import Any

from .episodic_memory import EpisodicMemory
from .semantic_memory import KnowledgeTriple, SemanticMemory


class ForgettingMechanism:
    """Delete outdated/wrong information."""

    def __init__(
        self,
        decay_rate: float = 0.1,
        confidence_threshold: float = 0.3,
        contradiction_threshold: int = 3,
    ) -> None:
        self.decay_rate = decay_rate
        self.confidence_threshold = confidence_threshold
        self.contradiction_threshold = contradiction_threshold

    def forget_episodic(self, episodic_memory: EpisodicMemory, days: int = 30) -> dict[str, Any]:
        """Forget old episodic memories using decay function."""
        now = datetime.now()
        initial_count = len(episodic_memory.episodes)

        # Calculate retention score for each episode
        retained = []
        for episode in episodic_memory.episodes:
            age_days = (now - episode.timestamp).days
            retention_score = self._retention_score(age_days, episode.success)

            if retention_score > self.confidence_threshold:
                retained.append(episode)

        episodic_memory.episodes = retained
        forgotten_count = initial_count - len(retained)

        return {
            "initial_episodes": initial_count,
            "forgotten_episodes": forgotten_count,
            "retained_episodes": len(retained),
            "forget_rate": forgotten_count / initial_count if initial_count > 0 else 0,
        }

    def forget_semantic(self, semantic_memory: SemanticMemory) -> dict[str, Any]:
        """Forget low-confidence and contradictory knowledge."""
        initial_count = len(semantic_memory.graph.triples)

        # Remove low-confidence knowledge
        semantic_memory.graph.triples = [
            t for t in semantic_memory.graph.triples if t.confidence >= self.confidence_threshold
        ]

        # Detect and remove contradictions
        contradictions = self._find_contradictions(semantic_memory.graph.triples)
        for triple in contradictions:
            if triple in semantic_memory.graph.triples:
                semantic_memory.graph.triples.remove(triple)

        forgotten_count = initial_count - len(semantic_memory.graph.triples)

        return {
            "initial_knowledge": initial_count,
            "forgotten_knowledge": forgotten_count,
            "retained_knowledge": len(semantic_memory.graph.triples),
            "contradictions_removed": len(contradictions),
        }

    def _retention_score(self, age_days: int, success: bool) -> float:
        """Calculate retention score using exponential decay."""
        # Ebbinghaus forgetting curve: R(t) = e^(-t/S)
        base_retention = math.exp(-age_days * self.decay_rate)

        # Successful memories decay slower
        if success:
            base_retention *= 1.5

        return min(base_retention, 1.0)

    def _find_contradictions(self, triples: list[KnowledgeTriple]) -> list[KnowledgeTriple]:
        """Find contradictory knowledge triples."""
        contradictions = []

        # Group by (subject, relation)
        groups: dict[tuple[str, str], list[KnowledgeTriple]] = {}
        for triple in triples:
            key = (triple.subject, triple.relation)
            if key not in groups:
                groups[key] = []
            groups[key].append(triple)

        # Find groups with multiple different objects
        for key, group in groups.items():
            if len(group) > 1:
                objects = [t.object for t in group]
                if len(set(objects)) > 1:  # Contradictory
                    # Keep highest confidence, mark others for deletion
                    sorted_group = sorted(group, key=lambda t: t.confidence, reverse=True)
                    contradictions.extend(sorted_group[1:])

        return contradictions
