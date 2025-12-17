"""Abductive reasoning - Infer best explanation."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Hypothesis:
    """A possible explanation."""

    explanation: str
    likelihood: float
    evidence: list[str]


class AbductiveReasoner:
    """Infer best explanation ('floor wet → probably spill')."""

    def __init__(self) -> None:
        self.explanation_rules: dict[str, list[tuple[str, float]]] = {}
        self._init_common_explanations()

    def _init_common_explanations(self) -> None:
        """Initialize common observation-explanation pairs."""
        self.explanation_rules = {
            "floor_wet": [
                ("liquid_spilled", 0.70),
                ("mopped_recently", 0.20),
                ("leak_from_ceiling", 0.10),
            ],
            "object_missing": [
                ("moved_by_human", 0.60),
                ("fell_behind_furniture", 0.25),
                ("taken_by_pet", 0.15),
            ],
            "light_off": [
                ("switch_turned_off", 0.50),
                ("bulb_burned_out", 0.30),
                ("power_outage", 0.20),
            ],
            "noise_detected": [
                ("object_dropped", 0.40),
                ("door_closed", 0.30),
                ("human_activity", 0.30),
            ],
            "temperature_high": [
                ("heater_on", 0.50),
                ("sunlight_exposure", 0.30),
                ("poor_ventilation", 0.20),
            ],
        }

    def infer_explanation(self, observation: str, evidence: list[str] | None = None) -> list[Hypothesis]:
        """Infer best explanation for observation."""
        if observation not in self.explanation_rules:
            return []

        hypotheses = []
        for explanation, base_likelihood in self.explanation_rules[observation]:
            # Adjust likelihood based on evidence
            adjusted_likelihood = base_likelihood
            supporting_evidence = []

            if evidence:
                for ev in evidence:
                    if self._supports(ev, explanation):
                        adjusted_likelihood *= 1.2
                        supporting_evidence.append(ev)
                    elif self._contradicts(ev, explanation):
                        adjusted_likelihood *= 0.5

            adjusted_likelihood = min(adjusted_likelihood, 0.99)
            hypotheses.append(
                Hypothesis(explanation, adjusted_likelihood, supporting_evidence)
            )

        return sorted(hypotheses, key=lambda h: h.likelihood, reverse=True)

    def best_explanation(self, observation: str, evidence: list[str] | None = None) -> Hypothesis | None:
        """Get single best explanation."""
        hypotheses = self.infer_explanation(observation, evidence)
        return hypotheses[0] if hypotheses else None

    def add_explanation_rule(self, observation: str, explanation: str, likelihood: float) -> None:
        """Add new explanation rule."""
        if observation not in self.explanation_rules:
            self.explanation_rules[observation] = []
        self.explanation_rules[observation].append((explanation, likelihood))

    def _supports(self, evidence: str, explanation: str) -> bool:
        """Check if evidence supports explanation."""
        support_map = {
            "liquid_spilled": ["cup_nearby", "liquid_trail", "wet_object"],
            "mopped_recently": ["mop_visible", "cleaning_smell"],
            "switch_turned_off": ["switch_down", "human_nearby"],
            "bulb_burned_out": ["old_bulb", "flickering_before"],
        }
        return evidence in support_map.get(explanation, [])

    def _contradicts(self, evidence: str, explanation: str) -> bool:
        """Check if evidence contradicts explanation."""
        contradiction_map = {
            "liquid_spilled": ["floor_dry_earlier", "no_liquids_nearby"],
            "power_outage": ["other_lights_on", "electronics_working"],
        }
        return evidence in contradiction_map.get(explanation, [])
