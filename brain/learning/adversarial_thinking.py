"""Adversarial Thinking - Predict what could go wrong and plan defenses."""
from dataclasses import dataclass
from typing import Any

from brain.planner.actions import Action


@dataclass
class Threat:
    threat_type: str
    description: str
    probability: float
    severity: float
    affected_actions: list[int]


@dataclass
class Countermeasure:
    threat: str
    strategy: str
    backup_actions: list[Action]
    risk_reduction: float


class AdversarialPlanner:
    def __init__(self):
        self.threat_database = {
            "navigate": ["human_trips", "obstacle_appears", "floor_slippery", "path_blocked"],
            "grasp": ["object_breaks", "grip_fails", "object_slips", "too_heavy"],
            "pour": ["spill", "container_tips", "liquid_splashes"],
            "release": ["object_drops", "placement_unstable"],
            "power": ["battery_dies", "power_outage", "motor_failure"]
        }
        self.threats_predicted = 0
        self.countermeasures_generated = 0

    def predict_threats(self, plan: list[Action], context: dict[str, Any] = None) -> list[Threat]:
        """Predict what could go wrong with a plan."""
        threats = []
        context = context or {}

        for i, action in enumerate(plan):
            action_type = action.action_type

            # Get potential threats for this action type
            if action_type in self.threat_database:
                for threat_type in self.threat_database[action_type]:
                    threat = self._analyze_threat(threat_type, action, i, context)
                    if threat.probability > 0.1:
                        threats.append(threat)

            # Environmental threats
            if context.get("crowded"):
                threats.append(Threat(
                    threat_type="human_collision",
                    description="Human might walk into robot's path",
                    probability=0.6,
                    severity=0.8,
                    affected_actions=[i]
                ))

            if context.get("low_battery"):
                threats.append(Threat(
                    threat_type="battery_dies",
                    description="Battery might die mid-task",
                    probability=0.7,
                    severity=0.9,
                    affected_actions=list(range(i, len(plan)))
                ))

        self.threats_predicted += len(threats)
        return threats

    def _analyze_threat(self, threat_type: str, action: Action,
                       action_idx: int, context: dict[str, Any]) -> Threat:
        """Analyze specific threat probability and severity."""
        base_probability = 0.2
        severity = 0.5

        # Adjust based on context
        if threat_type == "human_trips" and context.get("crowded"):
            base_probability = 0.5
            severity = 0.8
        elif threat_type == "object_breaks" and context.get("fragile"):
            base_probability = 0.4
            severity = 0.9
        elif threat_type == "floor_slippery" and context.get("wet_floor"):
            base_probability = 0.6
            severity = 0.7
        elif threat_type == "battery_dies" and context.get("low_battery"):
            base_probability = 0.7
            severity = 0.9
        elif threat_type == "spill" and action.action_type == "pour":
            base_probability = 0.3
            severity = 0.6

        return Threat(
            threat_type=threat_type,
            description=self._get_threat_description(threat_type),
            probability=base_probability,
            severity=severity,
            affected_actions=[action_idx]
        )

    def _get_threat_description(self, threat_type: str) -> str:
        """Get human-readable threat description."""
        descriptions = {
            "human_trips": "Human might trip over robot",
            "obstacle_appears": "New obstacle might block path",
            "floor_slippery": "Floor might be slippery",
            "path_blocked": "Path might become blocked",
            "object_breaks": "Object might break during handling",
            "grip_fails": "Gripper might fail to hold object",
            "object_slips": "Object might slip from grip",
            "too_heavy": "Object might be too heavy",
            "spill": "Liquid might spill",
            "container_tips": "Container might tip over",
            "liquid_splashes": "Liquid might splash",
            "object_drops": "Object might drop",
            "placement_unstable": "Placement might be unstable",
            "battery_dies": "Battery might die mid-task",
            "power_outage": "Power might go out",
            "motor_failure": "Motor might fail"
        }
        return descriptions.get(threat_type, "Unknown threat")

    def generate_backup_plans(self, threats: list[Threat],
                             original_plan: list[Action]) -> list[Countermeasure]:
        """Generate countermeasures for identified threats."""
        countermeasures = []

        for threat in threats:
            if threat.probability * threat.severity > 0.3:  # High risk
                countermeasure = self._create_countermeasure(threat, original_plan)
                countermeasures.append(countermeasure)

        self.countermeasures_generated += len(countermeasures)
        return countermeasures

    def _create_countermeasure(self, threat: Threat,
                              original_plan: list[Action]) -> Countermeasure:
        """Create specific countermeasure for a threat."""
        backup_actions = []
        strategy = ""
        risk_reduction = 0.0

        if threat.threat_type == "human_trips":
            strategy = "Announce presence and slow down"
            backup_actions = [
                Action(action_type="announce", parameters={"message": "Robot approaching"}),
                Action(action_type="reduce_speed", parameters={"speed": 0.3}),
                Action(action_type="monitor_humans", parameters={"distance": 2.0})
            ]
            risk_reduction = 0.6

        elif threat.threat_type == "object_breaks":
            strategy = "Use softer grip and slower movements"
            backup_actions = [
                Action(action_type="adjust_grip", parameters={"force": "minimal"}),
                Action(action_type="reduce_speed", parameters={"speed": 0.2}),
                Action(action_type="support_from_bottom", parameters={})
            ]
            risk_reduction = 0.7

        elif threat.threat_type == "battery_dies":
            strategy = "Charge immediately before continuing"
            backup_actions = [
                Action(action_type="navigate", location="charging_station", parameters={}),
                Action(action_type="charge", parameters={"duration": 300}),
                Action(action_type="resume_plan", parameters={})
            ]
            risk_reduction = 0.9

        elif threat.threat_type == "spill":
            strategy = "Pour slowly with spill detection"
            backup_actions = [
                Action(action_type="stabilize_container", parameters={}),
                Action(action_type="pour", parameters={"speed": "slow"}),
                Action(action_type="monitor_spill", parameters={})
            ]
            risk_reduction = 0.5

        elif threat.threat_type == "floor_slippery":
            strategy = "Navigate carefully with traction control"
            backup_actions = [
                Action(action_type="enable_traction_control", parameters={}),
                Action(action_type="reduce_speed", parameters={"speed": 0.4}),
                Action(action_type="test_surface", parameters={})
            ]
            risk_reduction = 0.6

        else:
            strategy = "Monitor and pause if threat materializes"
            backup_actions = [
                Action(action_type="monitor_threat", target=threat.threat_type, parameters={}),
                Action(action_type="pause_if_detected", parameters={})
            ]
            risk_reduction = 0.4

        return Countermeasure(
            threat=threat.threat_type,
            strategy=strategy,
            backup_actions=backup_actions,
            risk_reduction=risk_reduction
        )

    def get_adversarial_stats(self) -> dict[str, Any]:
        """Get statistics on adversarial thinking."""
        return {
            "threats_predicted": self.threats_predicted,
            "countermeasures_generated": self.countermeasures_generated,
            "threat_categories": len(self.threat_database),
            "avg_countermeasures_per_threat": self.countermeasures_generated / max(1, self.threats_predicted)
        }
