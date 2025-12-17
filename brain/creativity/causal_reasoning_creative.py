"""Causal reasoning for creative problem solving - predict outcomes and risks."""

from typing import Any


class CausalReasoningCreative:
    """Build causal models to predict action outcomes."""

    def __init__(self) -> None:
        self.causal_rules = self._build_causal_rules()

    def predict_outcome(
        self, action: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """Predict outcome of action in given context."""
        causal_chain = self.build_causal_chain(action, context)
        risks = self.identify_risks(causal_chain)
        opportunities = self.identify_opportunities(causal_chain)

        return {
            "action": action,
            "causal_chain": causal_chain,
            "risks": risks,
            "opportunities": opportunities,
            "overall_risk_level": self._calculate_risk_level(risks),
        }

    def build_causal_chain(
        self, action: dict[str, Any], context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Build chain of cause-effect relationships."""
        chain = [{"event": "action", "description": action.get("type", "unknown")}]

        action_type = action.get("type", "")

        # Apply causal rules
        for rule in self.causal_rules:
            if self._rule_applies(rule, action_type, context):
                effect = rule["effect"].copy()
                effect["probability"] = self._calculate_probability(rule, context)
                chain.append(effect)

                # Check for cascading effects
                if effect.get("triggers"):
                    for trigger in effect["triggers"]:
                        chain.append(trigger)

        return chain

    def identify_risks(self, causal_chain: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Identify potential risks in causal chain."""
        risks = []

        for event in causal_chain:
            if event.get("type") == "negative":
                risks.append(
                    {
                        "risk": event["description"],
                        "severity": event.get("severity", "medium"),
                        "probability": event.get("probability", 0.5),
                        "mitigation": event.get("mitigation", "Monitor carefully"),
                    }
                )

        return risks

    def identify_opportunities(
        self, causal_chain: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Identify potential opportunities in causal chain."""
        opportunities = []

        for event in causal_chain:
            if event.get("type") == "positive":
                opportunities.append(
                    {
                        "opportunity": event["description"],
                        "benefit": event.get("benefit", "medium"),
                        "probability": event.get("probability", 0.5),
                    }
                )

        return opportunities

    def _rule_applies(
        self, rule: dict[str, Any], action_type: str, context: dict[str, Any]
    ) -> bool:
        """Check if causal rule applies to action and context."""
        if rule["action"] != action_type:
            return False

        for condition in rule.get("conditions", []):
            if not self._check_condition(condition, context):
                return False

        return True

    def _check_condition(self, condition: dict[str, Any], context: dict[str, Any]) -> bool:
        """Check if condition is met in context."""
        key = condition["key"]
        expected = condition["value"]
        actual = context.get(key)

        operator = condition.get("operator")
        if operator == "equals":
            return bool(actual == expected)
        if operator == "greater_than":
            return bool(actual is not None and actual > expected)
        if operator == "less_than":
            return bool(actual is not None and actual < expected)
        if operator == "contains":
            return bool(actual is not None and expected in actual)

        return False

    def _calculate_probability(
        self, rule: dict[str, Any], context: dict[str, Any]
    ) -> float:
        """Calculate probability of effect occurring."""
        base_prob = float(rule.get("base_probability", 0.5))

        # Adjust based on context factors
        for modifier in rule.get("probability_modifiers", []):
            if self._check_condition(modifier["condition"], context):
                base_prob *= float(modifier["multiplier"])

        return float(min(max(base_prob, 0.0), 1.0))

    def _calculate_risk_level(self, risks: list[dict[str, Any]]) -> str:
        """Calculate overall risk level."""
        if not risks:
            return "low"

        max_severity = max(
            (
                {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(
                    r["severity"], 2
                )
                for r in risks
            ),
            default=1,
        )

        if max_severity >= 4:
            return "critical"
        if max_severity >= 3:
            return "high"
        if max_severity >= 2:
            return "medium"
        return "low"

    def _build_causal_rules(self) -> list[dict[str, Any]]:
        """Build library of causal rules."""
        return [
            {
                "action": "push",
                "conditions": [
                    {"key": "object_near_edge", "value": True, "operator": "equals"}
                ],
                "effect": {
                    "type": "negative",
                    "description": "Object falls off edge",
                    "severity": "high",
                    "mitigation": "Move away from edge first",
                },
                "base_probability": 0.8,
            },
            {
                "action": "grasp",
                "conditions": [
                    {"key": "object_fragile", "value": True, "operator": "equals"}
                ],
                "effect": {
                    "type": "negative",
                    "description": "Object might break",
                    "severity": "medium",
                    "mitigation": "Use gentle grip force",
                },
                "base_probability": 0.3,
            },
            {
                "action": "navigate_to",
                "conditions": [{"key": "floor_wet", "value": True, "operator": "equals"}],
                "effect": {
                    "type": "negative",
                    "description": "Might slip on wet floor",
                    "severity": "high",
                    "mitigation": "Reduce speed, increase stability",
                },
                "base_probability": 0.6,
            },
            {
                "action": "clean",
                "conditions": [],
                "effect": {
                    "type": "positive",
                    "description": "Area becomes clean",
                    "benefit": "high",
                    "triggers": [
                        {
                            "type": "positive",
                            "description": "Human satisfaction increases",
                            "benefit": "medium",
                        }
                    ],
                },
                "base_probability": 0.9,
            },
        ]
