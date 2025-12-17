"""Conceptual blending - combine concepts to create new ideas."""

from typing import Any


class ConceptualBlending:
    """Blend concepts to generate novel solutions."""

    def __init__(self) -> None:
        self.concept_library = self._build_concept_library()

    def blend_concepts(
        self, concept_a: str, concept_b: str
    ) -> dict[str, Any]:
        """Combine two concepts to create new idea."""
        data_a = self.concept_library.get(concept_a)
        data_b = self.concept_library.get(concept_b)

        if not data_a or not data_b:
            return {
                "success": False,
                "message": "One or both concepts not found",
            }

        shared = self.find_commonalities(data_a, data_b)
        novel = self.combine_unique_features(data_a, data_b)
        new_concept = self.synthesize_new_concept(shared, novel, concept_a, concept_b)

        return {
            "success": True,
            "concept_a": concept_a,
            "concept_b": concept_b,
            "shared_features": shared,
            "novel_features": novel,
            "new_concept": new_concept,
        }

    def find_commonalities(
        self, concept_a: dict[str, Any], concept_b: dict[str, Any]
    ) -> list[str]:
        """Find shared features between concepts."""
        features_a = set(concept_a.get("features", []))
        features_b = set(concept_b.get("features", []))
        return list(features_a & features_b)

    def combine_unique_features(
        self, concept_a: dict[str, Any], concept_b: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Combine unique features from both concepts."""
        features_a = set(concept_a.get("features", []))
        features_b = set(concept_b.get("features", []))

        unique_a = features_a - features_b
        unique_b = features_b - features_a

        combined = []
        for feat in unique_a:
            combined.append({"feature": feat, "source": concept_a["name"]})
        for feat in unique_b:
            combined.append({"feature": feat, "source": concept_b["name"]})

        return combined

    def synthesize_new_concept(
        self,
        shared: list[str],
        novel: list[dict[str, Any]],
        name_a: str,
        name_b: str,
    ) -> dict[str, Any]:
        """Synthesize new concept from components."""
        # Generate name
        new_name = f"{name_a}_{name_b}_blend"

        # Combine capabilities
        capabilities = []
        for feature in shared:
            capabilities.append(f"Enhanced {feature}")

        for item in novel:
            capabilities.append(f"{item['feature']} from {item['source']}")

        # Generate description
        description = f"A novel concept combining {name_a} and {name_b}"

        # Calculate novelty score
        novelty = len(novel) / max(len(novel) + len(shared), 1)

        return {
            "name": new_name,
            "description": description,
            "capabilities": capabilities,
            "novelty_score": novelty,
            "practical_applications": self._generate_applications(
                name_a, name_b, capabilities
            ),
        }

    def _generate_applications(
        self, concept_a: str, concept_b: str, capabilities: list[str]
    ) -> list[str]:
        """Generate practical applications for blended concept."""
        applications = []

        # Pattern-based application generation
        if "vacuum" in concept_a and "lawn_mower" in concept_b:
            applications.append("Autonomous floor cleaning robot")
            applications.append("Outdoor debris collection system")

        if "delivery" in concept_a and "drone" in concept_b:
            applications.append("Aerial package delivery")
            applications.append("Emergency supply transport")

        if "camera" in concept_a and "security" in concept_b:
            applications.append("Intelligent surveillance system")
            applications.append("Automated threat detection")

        # Generic applications based on capabilities
        if len(capabilities) > 3:
            applications.append("Multi-purpose automation tool")

        return applications if applications else ["Novel automation solution"]

    def _build_concept_library(self) -> dict[str, dict[str, Any]]:
        """Build library of concepts with features."""
        return {
            "vacuum_cleaner": {
                "name": "vacuum_cleaner",
                "features": ["suction", "mobility", "debris_collection", "automated"],
                "domain": "cleaning",
            },
            "lawn_mower": {
                "name": "lawn_mower",
                "features": [
                    "cutting",
                    "mobility",
                    "outdoor",
                    "automated",
                    "navigation",
                ],
                "domain": "gardening",
            },
            "delivery": {
                "name": "delivery",
                "features": ["transport", "navigation", "package_handling", "routing"],
                "domain": "logistics",
            },
            "drone": {
                "name": "drone",
                "features": ["flight", "aerial", "navigation", "camera", "automated"],
                "domain": "aviation",
            },
            "camera": {
                "name": "camera",
                "features": ["vision", "recording", "detection", "monitoring"],
                "domain": "sensing",
            },
            "security": {
                "name": "security",
                "features": ["monitoring", "detection", "alert", "protection"],
                "domain": "safety",
            },
            "assistant": {
                "name": "assistant",
                "features": [
                    "communication",
                    "task_execution",
                    "learning",
                    "interaction",
                ],
                "domain": "service",
            },
            "robot_arm": {
                "name": "robot_arm",
                "features": [
                    "manipulation",
                    "precision",
                    "grasping",
                    "positioning",
                ],
                "domain": "manipulation",
            },
        }

    def suggest_blends(self, goal: str) -> list[dict[str, Any]]:
        """Suggest concept blends for achieving goal."""
        suggestions = []

        goal_lower = goal.lower()

        if "clean" in goal_lower and "outdoor" in goal_lower:
            suggestions.append(
                self.blend_concepts("vacuum_cleaner", "lawn_mower")
            )

        if "deliver" in goal_lower and "fast" in goal_lower:
            suggestions.append(self.blend_concepts("delivery", "drone"))

        if "monitor" in goal_lower or "security" in goal_lower:
            suggestions.append(self.blend_concepts("camera", "security"))

        return suggestions
