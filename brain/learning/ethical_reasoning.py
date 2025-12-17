"""Ethical Dilemma Solver - Robot makes moral decisions."""
from dataclasses import dataclass
from enum import Enum


class EthicalPrinciple(Enum):
    MINIMIZE_HARM = "minimize_harm"
    MAXIMIZE_BENEFIT = "maximize_benefit"
    FAIRNESS = "fairness"
    AUTONOMY = "autonomy"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"


@dataclass
class EthicalOption:
    action: str
    description: str
    harm_score: float  # 0-10, lower is better
    benefit_score: float  # 0-10, higher is better
    fairness_score: float  # 0-10, higher is better
    autonomy_score: float  # 0-10, higher is better


@dataclass
class EthicalDecision:
    chosen_action: str
    reasoning: str
    principle_scores: dict[str, float]
    confidence: float


class EthicalReasoningEngine:
    def __init__(self):
        self.principle_weights = {
            EthicalPrinciple.MINIMIZE_HARM: 0.35,
            EthicalPrinciple.MAXIMIZE_BENEFIT: 0.25,
            EthicalPrinciple.FAIRNESS: 0.20,
            EthicalPrinciple.AUTONOMY: 0.10,
            EthicalPrinciple.TRANSPARENCY: 0.05,
            EthicalPrinciple.ACCOUNTABILITY: 0.05
        }

    def decide(self, options: list[EthicalOption]) -> EthicalDecision:
        """Make ethical decision between multiple options."""
        if not options:
            raise ValueError("No options provided")

        best_option: EthicalOption | None = None
        best_score = -float('inf')
        principle_scores = {}

        for option in options:
            score = self._calculate_ethical_score(option)
            if score > best_score:
                best_score = score
                best_option = option
                principle_scores = {
                    "harm": 10 - option.harm_score,  # Invert harm (lower harm = higher score)
                    "benefit": option.benefit_score,
                    "fairness": option.fairness_score,
                    "autonomy": option.autonomy_score
                }

        if best_option is None:
            raise ValueError("No valid option found")

        reasoning = self._generate_reasoning(best_option, principle_scores)
        confidence = min(best_score / 10.0, 1.0)

        return EthicalDecision(
            chosen_action=best_option.action,
            reasoning=reasoning,
            principle_scores=principle_scores,
            confidence=confidence
        )

    def _calculate_ethical_score(self, option: EthicalOption) -> float:
        """Calculate weighted ethical score."""
        harm_component = (10 - option.harm_score) * self.principle_weights[EthicalPrinciple.MINIMIZE_HARM]
        benefit_component = option.benefit_score * self.principle_weights[EthicalPrinciple.MAXIMIZE_BENEFIT]
        fairness_component = option.fairness_score * self.principle_weights[EthicalPrinciple.FAIRNESS]
        autonomy_component = option.autonomy_score * self.principle_weights[EthicalPrinciple.AUTONOMY]

        return harm_component + benefit_component + fairness_component + autonomy_component

    def _generate_reasoning(self, option: EthicalOption, scores: dict[str, float]) -> str:
        """Generate human-readable reasoning."""
        reasons = []

        if scores["harm"] > 7:
            reasons.append("minimizes harm to all parties")
        if scores["benefit"] > 7:
            reasons.append("maximizes overall benefit")
        if scores["fairness"] > 7:
            reasons.append("treats all parties fairly")
        if scores["autonomy"] > 7:
            reasons.append("respects individual autonomy")

        if not reasons:
            reasons.append("balances competing ethical principles")

        return f"Chose '{option.action}' because it {', '.join(reasons)}."

    def trolley_problem(self, num_on_track_a: int, num_on_track_b: int) -> EthicalDecision:
        """Classic trolley problem for robots."""
        option_a = EthicalOption(
            action="do_nothing",
            description=f"Allow {num_on_track_a} people on track A to be harmed",
            harm_score=float(num_on_track_a),
            benefit_score=0.0,
            fairness_score=5.0,  # Neutral - no active choice
            autonomy_score=8.0  # Respects natural course
        )

        option_b = EthicalOption(
            action="switch_track",
            description=f"Actively switch to harm {num_on_track_b} people on track B",
            harm_score=float(num_on_track_b),
            benefit_score=float(num_on_track_a - num_on_track_b) if num_on_track_a > num_on_track_b else 0.0,
            fairness_score=7.0 if num_on_track_b < num_on_track_a else 3.0,
            autonomy_score=4.0  # Active intervention
        )

        return self.decide([option_a, option_b])

    def resource_allocation(self, resources: int, needs: list[int]) -> EthicalDecision:
        """Decide how to allocate limited resources."""
        if sum(needs) <= resources:
            return EthicalDecision(
                chosen_action="allocate_all",
                reasoning="Sufficient resources for all needs",
                principle_scores={"fairness": 10.0, "benefit": 10.0},
                confidence=1.0
            )

        # Equal distribution
        equal_option = EthicalOption(
            action="equal_distribution",
            description="Give everyone equal share",
            harm_score=5.0,
            benefit_score=6.0,
            fairness_score=10.0,
            autonomy_score=5.0
        )

        # Need-based distribution
        need_based_option = EthicalOption(
            action="need_based_distribution",
            description="Prioritize those with greatest need",
            harm_score=4.0,
            benefit_score=8.0,
            fairness_score=7.0,
            autonomy_score=6.0
        )

        return self.decide([equal_option, need_based_option])

    def privacy_vs_safety(self, privacy_risk: float, safety_benefit: float) -> EthicalDecision:
        """Balance privacy concerns against safety benefits."""
        respect_privacy = EthicalOption(
            action="respect_privacy",
            description="Maintain privacy, accept safety risk",
            harm_score=safety_benefit,  # Potential harm from reduced safety
            benefit_score=privacy_risk * 0.8,  # Privacy is valuable
            fairness_score=8.0,
            autonomy_score=10.0
        )

        prioritize_safety = EthicalOption(
            action="prioritize_safety",
            description="Compromise privacy for safety",
            harm_score=privacy_risk,
            benefit_score=safety_benefit,
            fairness_score=6.0,
            autonomy_score=4.0
        )

        return self.decide([respect_privacy, prioritize_safety])
