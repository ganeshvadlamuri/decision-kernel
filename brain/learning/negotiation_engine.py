"""Negotiation Engine - Robot negotiates with humans when goals conflict."""
from dataclasses import dataclass
from typing import Any


@dataclass
class Constraint:
    type: str
    description: str
    severity: float
    negotiable: bool


@dataclass
class Proposal:
    description: str
    robot_satisfaction: float
    human_satisfaction: float
    compromise_level: float


@dataclass
class NegotiationResult:
    agreed: bool
    final_proposal: str
    robot_satisfaction: float
    human_satisfaction: float
    negotiation_rounds: int


class NegotiationEngine:
    def __init__(self):
        self.negotiation_history: list[NegotiationResult] = []
        self.negotiation_count = 0

    def negotiate_with_human(self, human_request: str,
                            robot_constraint: str,
                            context: dict[str, Any] | None = None) -> NegotiationResult:
        """Negotiate when human request conflicts with robot constraints."""
        context = context or {}

        # Analyze constraints
        human_constraint = self._analyze_human_need(human_request, context)
        robot_needs = self._analyze_robot_constraint(robot_constraint, context)

        # Generate proposals
        proposals = self._generate_proposals(human_request, robot_constraint,
                                            human_constraint, robot_needs, context)

        # Select best proposal
        best_proposal = self._select_best_proposal(proposals)

        # Simulate negotiation rounds
        rounds = self._simulate_negotiation(human_constraint, robot_needs, best_proposal)

        result = NegotiationResult(
            agreed=True,
            final_proposal=best_proposal.description,
            robot_satisfaction=best_proposal.robot_satisfaction,
            human_satisfaction=best_proposal.human_satisfaction,
            negotiation_rounds=rounds
        )

        self.negotiation_history.append(result)
        self.negotiation_count += 1

        return result

    def _analyze_human_need(self, request: str, context: dict[str, Any]) -> Constraint:
        """Analyze human's need and urgency."""
        request_lower = request.lower()

        if "now" in request_lower or "immediately" in request_lower:
            return Constraint(
                type="urgency",
                description="Human needs immediate action",
                severity=0.9,
                negotiable=False
            )
        elif "clean" in request_lower:
            return Constraint(
                type="cleanliness",
                description="Human wants clean environment",
                severity=0.6,
                negotiable=True
            )
        elif "bring" in request_lower or "fetch" in request_lower:
            return Constraint(
                type="delivery",
                description="Human needs object delivered",
                severity=0.7,
                negotiable=True
            )
        else:
            return Constraint(
                type="general",
                description="General human request",
                severity=0.5,
                negotiable=True
            )

    def _analyze_robot_constraint(self, constraint: str, context: dict[str, Any]) -> Constraint:
        """Analyze robot's constraint."""
        constraint_lower = constraint.lower()

        if "battery" in constraint_lower or "low_battery" in constraint_lower:
            battery_level = context.get("battery_level", 5)
            return Constraint(
                type="battery",
                description=f"Battery at {battery_level}%",
                severity=0.9 if battery_level < 10 else 0.7,
                negotiable=True
            )
        elif "busy" in constraint_lower or "task" in constraint_lower:
            return Constraint(
                type="busy",
                description="Currently executing another task",
                severity=0.6,
                negotiable=True
            )
        elif "maintenance" in constraint_lower:
            return Constraint(
                type="maintenance",
                description="Needs maintenance",
                severity=0.8,
                negotiable=False
            )
        else:
            return Constraint(
                type="general",
                description="General robot constraint",
                severity=0.5,
                negotiable=True
            )

    def _generate_proposals(self, human_request: str, robot_constraint: str,
                           human_need: Constraint, robot_need: Constraint,
                           context: dict[str, Any]) -> list[Proposal]:
        """Generate negotiation proposals."""
        proposals = []

        # Proposal 1: Partial fulfillment
        if robot_need.type == "battery":
            proposals.append(Proposal(
                description=f"I can {human_request.lower()} for 10 minutes, then charge, then finish",
                robot_satisfaction=0.7,
                human_satisfaction=0.6,
                compromise_level=0.5
            ))

        # Proposal 2: Delayed fulfillment
        if robot_need.negotiable:
            delay_time = "30 minutes" if robot_need.severity > 0.7 else "15 minutes"
            proposals.append(Proposal(
                description=f"I can {human_request.lower()} in {delay_time} after addressing {robot_constraint}",
                robot_satisfaction=0.9,
                human_satisfaction=0.5,
                compromise_level=0.4
            ))

        # Proposal 3: Alternative solution
        if "clean" in human_request.lower():
            proposals.append(Proposal(
                description="I can clean the high-priority areas now, and do a full clean later",
                robot_satisfaction=0.8,
                human_satisfaction=0.7,
                compromise_level=0.6
            ))

        # Proposal 4: Immediate action with limitations
        proposals.append(Proposal(
            description=f"I'll {human_request.lower()} immediately, but may need to pause for {robot_constraint}",
            robot_satisfaction=0.5,
            human_satisfaction=0.8,
            compromise_level=0.7
        ))

        # Proposal 5: Request human help
        if robot_need.type == "battery":
            proposals.append(Proposal(
                description="Could you plug me in while I work? Then I can complete the task without interruption",
                robot_satisfaction=0.9,
                human_satisfaction=0.8,
                compromise_level=0.3
            ))

        return proposals

    def _select_best_proposal(self, proposals: list[Proposal]) -> Proposal:
        """Select proposal that maximizes joint satisfaction."""
        if not proposals:
            return Proposal(
                description="Let me try my best",
                robot_satisfaction=0.5,
                human_satisfaction=0.5,
                compromise_level=0.5
            )

        # Score = (human_satisfaction + robot_satisfaction) / 2
        best = max(proposals, key=lambda p: (p.human_satisfaction + p.robot_satisfaction) / 2)
        return best

    def _simulate_negotiation(self, human_need: Constraint,
                             robot_need: Constraint, proposal: Proposal) -> int:
        """Simulate negotiation rounds."""
        if not human_need.negotiable and not robot_need.negotiable:
            return 1  # Quick agreement or rejection

        if proposal.compromise_level < 0.3:
            return 1  # Easy agreement
        elif proposal.compromise_level < 0.6:
            return 2  # Some discussion
        else:
            return 3  # Extended negotiation

    def get_negotiation_stats(self) -> dict[str, Any]:
        """Get negotiation statistics."""
        if not self.negotiation_history:
            return {"negotiations": 0}

        avg_robot_sat = sum(n.robot_satisfaction for n in self.negotiation_history) / len(self.negotiation_history)
        avg_human_sat = sum(n.human_satisfaction for n in self.negotiation_history) / len(self.negotiation_history)
        avg_rounds = sum(n.negotiation_rounds for n in self.negotiation_history) / len(self.negotiation_history)

        return {
            "total_negotiations": self.negotiation_count,
            "successful_negotiations": sum(1 for n in self.negotiation_history if n.agreed),
            "avg_robot_satisfaction": f"{avg_robot_sat:.2%}",
            "avg_human_satisfaction": f"{avg_human_sat:.2%}",
            "avg_negotiation_rounds": f"{avg_rounds:.1f}"
        }
