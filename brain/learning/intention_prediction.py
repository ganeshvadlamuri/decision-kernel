"""Intention Prediction - Know what human wants before they ask."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class HumanContext:
    location: str
    time_of_day: datetime
    recent_actions: list[str]
    body_language: str
    gaze_direction: str


@dataclass
class PredictedIntent:
    intent: str
    confidence: float
    reasoning: str
    proactive_actions: list[str]


class IntentionPredictor:
    def __init__(self):
        self.intent_patterns: dict[str, list[dict[str, Any]]] = {
            "want_coffee": [
                {"time": (6, 9), "location": "kitchen", "confidence": 0.85},
                {"recent_action": "wake_up", "location": "kitchen", "confidence": 0.90},
                {"gaze": "coffee_maker", "confidence": 0.95}
            ],
            "want_water": [
                {"location": "kitchen", "gaze": "fridge", "confidence": 0.80},
                {"body_language": "tired", "confidence": 0.70}
            ],
            "want_to_sit": [
                {"body_language": "tired", "gaze": "chair", "confidence": 0.85},
                {"recent_action": "standing_long", "confidence": 0.75}
            ],
            "need_help": [
                {"body_language": "frustrated", "confidence": 0.80},
                {"recent_action": "failed_task", "confidence": 0.90}
            ],
            "want_entertainment": [
                {"time": (18, 23), "location": "living_room", "confidence": 0.70},
                {"body_language": "relaxed", "location": "couch", "confidence": 0.75}
            ],
            "want_food": [
                {"time": (11, 14), "location": "kitchen", "confidence": 0.80},
                {"time": (17, 20), "location": "kitchen", "confidence": 0.85},
                {"gaze": "fridge", "confidence": 0.75}
            ]
        }
        self.prediction_history: list[PredictedIntent] = []

    def predict_human_intention(self, context: HumanContext) -> PredictedIntent:
        """Predict what human wants before they ask."""
        best_intent = None
        best_confidence = 0.0
        best_reasoning = ""

        current_hour = context.time_of_day.hour

        for intent, patterns in self.intent_patterns.items():
            confidence = 0.0
            reasons = []

            for pattern in patterns:
                # Check time match
                if "time" in pattern:
                    time_range = pattern["time"]
                    if time_range[0] <= current_hour <= time_range[1]:
                        confidence += pattern["confidence"] * 0.4
                        reasons.append(f"time is {current_hour}:00")

                # Check location match
                if "location" in pattern and pattern["location"] == context.location:
                    confidence += pattern["confidence"] * 0.3
                    reasons.append(f"in {context.location}")

                # Check gaze match
                if "gaze" in pattern and pattern["gaze"] in context.gaze_direction:
                    confidence += pattern["confidence"] * 0.3
                    reasons.append(f"looking at {context.gaze_direction}")

                # Check body language
                if "body_language" in pattern and pattern["body_language"] == context.body_language:
                    confidence += pattern["confidence"] * 0.2
                    reasons.append(f"appears {context.body_language}")

                # Check recent actions
                if "recent_action" in pattern and pattern["recent_action"] in context.recent_actions:
                    confidence += pattern["confidence"] * 0.2
                    reasons.append(f"just {pattern['recent_action']}")

            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent
                best_reasoning = ", ".join(reasons)

        # Generate proactive actions
        proactive_actions = self._generate_proactive_actions(best_intent or "unknown")

        predicted = PredictedIntent(
            intent=best_intent or "unknown",
            confidence=min(best_confidence, 1.0),
            reasoning=best_reasoning or "no clear signals",
            proactive_actions=proactive_actions
        )

        self.prediction_history.append(predicted)
        return predicted

    def _generate_proactive_actions(self, intent: str) -> list[str]:
        """Generate actions to take before being asked."""
        actions_map = {
            "want_coffee": ["navigate_to_kitchen", "start_coffee_maker", "prepare_cup"],
            "want_water": ["navigate_to_kitchen", "get_water_bottle", "bring_to_human"],
            "want_to_sit": ["clear_chair", "adjust_cushion", "move_closer"],
            "need_help": ["approach_human", "ask_if_help_needed", "standby"],
            "want_entertainment": ["turn_on_tv", "suggest_activities", "prepare_games"],
            "want_food": ["check_fridge", "suggest_meal_options", "prepare_ingredients"]
        }
        return actions_map.get(intent, ["observe", "standby"])

    def get_prediction_accuracy(self) -> dict[str, Any]:
        """Calculate how accurate predictions have been."""
        if not self.prediction_history:
            return {"status": "no_predictions"}

        high_confidence = [p for p in self.prediction_history if p.confidence > 0.7]
        avg_confidence = sum(p.confidence for p in self.prediction_history) / len(self.prediction_history)

        return {
            "total_predictions": len(self.prediction_history),
            "high_confidence_predictions": len(high_confidence),
            "avg_confidence": f"{avg_confidence:.2%}",
            "most_predicted": max(set(p.intent for p in self.prediction_history),
                                key=lambda x: sum(1 for p in self.prediction_history if p.intent == x))
        }
