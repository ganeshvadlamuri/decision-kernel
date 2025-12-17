"""Semantic memory - Build knowledge graph."""

from dataclasses import dataclass
from typing import Any


@dataclass
class KnowledgeTriple:
    """A knowledge triple (subject, relation, object)."""

    subject: str
    relation: str
    object: str
    confidence: float = 1.0


class KnowledgeGraph:
    """Graph representation of semantic knowledge."""

    def __init__(self) -> None:
        self.triples: list[KnowledgeTriple] = []

    def add(self, subject: str, relation: str, obj: str, confidence: float = 1.0) -> None:
        """Add knowledge triple."""
        self.triples.append(KnowledgeTriple(subject, relation, obj, confidence))

    def query(self, subject: str | None = None, relation: str | None = None, obj: str | None = None) -> list[KnowledgeTriple]:
        """Query knowledge graph."""
        results = self.triples
        if subject:
            results = [t for t in results if t.subject == subject]
        if relation:
            results = [t for t in results if t.relation == relation]
        if obj:
            results = [t for t in results if t.object == obj]
        return results

    def get_properties(self, subject: str) -> dict[str, list[str]]:
        """Get all properties of a subject."""
        triples = self.query(subject=subject)
        properties: dict[str, list[str]] = {}
        for t in triples:
            if t.relation not in properties:
                properties[t.relation] = []
            properties[t.relation].append(t.object)
        return properties


class SemanticMemory:
    """Build knowledge graph (kitchen → has → coffee maker)."""

    def __init__(self) -> None:
        self.graph = KnowledgeGraph()

    def learn(self, subject: str, relation: str, obj: str, confidence: float = 1.0) -> None:
        """Learn new knowledge."""
        self.graph.add(subject, relation, obj, confidence)

    def knows(self, subject: str, relation: str, obj: str) -> bool:
        """Check if knowledge exists."""
        return len(self.graph.query(subject, relation, obj)) > 0

    def what_has(self, subject: str) -> list[str]:
        """What does subject have?"""
        triples = self.graph.query(subject=subject, relation="has")
        return [t.object for t in triples]

    def where_is(self, obj: str) -> list[str]:
        """Where is object located?"""
        triples = self.graph.query(relation="has", obj=obj)
        return [t.subject for t in triples]

    def get_all_knowledge(self, subject: str) -> dict[str, Any]:
        """Get all knowledge about subject."""
        return self.graph.get_properties(subject)

    def infer_transitive(self, relation: str) -> list[KnowledgeTriple]:
        """Infer transitive relations (A→B, B→C implies A→C)."""
        inferred = []
        triples = self.graph.query(relation=relation)

        for t1 in triples:
            for t2 in triples:
                if t1.object == t2.subject:
                    # A→B, B→C implies A→C
                    if not self.knows(t1.subject, relation, t2.object):
                        confidence = min(t1.confidence, t2.confidence) * 0.8
                        inferred.append(
                            KnowledgeTriple(t1.subject, relation, t2.object, confidence)
                        )

        return inferred
