"""Causal reasoning - Understand cause-effect relationships."""

from dataclasses import dataclass
from typing import Any


@dataclass
class CausalRelation:
    """A cause-effect relationship."""

    cause: str
    effect: str
    probability: float
    mechanism: str


class CausalReasoner:
    """Understand cause-effect ('if I push cup, it falls')."""

    def __init__(self) -> None:
        self.causal_model: list[CausalRelation] = []
        self._init_physics_rules()

    def _init_physics_rules(self) -> None:
        """Initialize basic physics causal rules."""
        rules = [
            ("push_object", "object_moves", 0.95, "force_transfer"),
            ("drop_object", "object_falls", 0.99, "gravity"),
            ("heat_water", "water_boils", 0.90, "thermal_energy"),
            ("flip_switch", "light_turns_on", 0.85, "electrical_circuit"),
            ("open_door", "air_flows", 0.80, "pressure_difference"),
            ("spill_liquid", "floor_wet", 0.95, "liquid_spread"),
            ("block_light", "shadow_forms", 0.99, "light_occlusion"),
            ("apply_force", "object_deforms", 0.70, "material_stress"),
        ]
        for cause, effect, prob, mech in rules:
            self.causal_model.append(CausalRelation(cause, effect, prob, mech))

    def predict_effect(self, cause: str) -> list[tuple[str, float]]:
        """Predict effects of a cause."""
        effects = []
        for relation in self.causal_model:
            if relation.cause == cause:
                effects.append((relation.effect, relation.probability))
        return sorted(effects, key=lambda x: x[1], reverse=True)

    def explain_effect(self, effect: str) -> list[tuple[str, str]]:
        """Explain possible causes of an effect."""
        causes = []
        for relation in self.causal_model:
            if relation.effect == effect:
                causes.append((relation.cause, relation.mechanism))
        return causes

    def learn_causal_relation(
        self, cause: str, effect: str, probability: float, mechanism: str = "learned"
    ) -> None:
        """Learn new causal relation from experience."""
        self.causal_model.append(CausalRelation(cause, effect, probability, mechanism))

    def will_cause(self, action: str, effect: str) -> tuple[bool, float]:
        """Check if action will cause effect."""
        for relation in self.causal_model:
            if relation.cause == action and relation.effect == effect:
                return True, relation.probability
        return False, 0.0

    def intervention_analysis(self, action: str) -> dict[str, Any]:
        """Analyze all effects of an intervention."""
        direct_effects = self.predict_effect(action)

        # Find indirect effects (chain reactions)
        indirect_effects = []
        for effect, prob in direct_effects:
            secondary = self.predict_effect(effect)
            for sec_effect, sec_prob in secondary:
                indirect_effects.append((sec_effect, prob * sec_prob))

        return {
            "action": action,
            "direct_effects": direct_effects,
            "indirect_effects": indirect_effects,
            "total_effects": len(direct_effects) + len(indirect_effects),
        }
