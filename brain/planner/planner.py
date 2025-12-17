
from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.skills.registry import SkillRegistry
from brain.world.state import WorldState


class Planner:
    """Naive symbolic planner for action sequence generation"""

    def __init__(self, skill_registry: SkillRegistry | None = None):
        self.skill_registry = skill_registry

    def plan(self, goal: Goal, world_state: WorldState) -> list[Action]:
        """Generate action sequence to achieve goal"""

        # Check if skill is registered
        if self.skill_registry:
            skill = self.skill_registry.get(goal.action)
            if skill:
                return self._plan_from_skill(skill, goal, world_state)

        # Fallback to naive planning
        # Social & Communication
        if goal.action == "greet":
            return [Action("speak", target="Hello! How can I help you?")]

        if goal.action == "status_report":
            return [Action("speak", target="I'm operational and ready to assist!")]

        if goal.action == "acknowledge":
            return [Action("speak", target="You're welcome!")]

        if goal.action == "answer_question":
            return [Action("speak", target=f"Let me help you with: {goal.target}")]

        if goal.action == "explain":
            return [Action("speak", target=f"Explaining {goal.target}...")]

        # Emotional Intelligence
        if goal.action == "emotional_support":
            return [
                Action("speak", target="I understand. Let me help you feel better."),
                Action("adjust_behavior", target="gentle_mode")
            ]

        # Learning & Improvement
        if goal.action == "learn_task":
            return [Action("record_demonstration", target=goal.target)]

        if goal.action == "self_improve":
            return [Action("analyze_performance", target="self")]

        # Exploration
        if goal.action == "explore":
            return [
                Action("navigate_to", location=goal.location),
                Action("scan_environment", location=goal.location)
            ]

        # Prediction & Planning
        if goal.action == "predict_future":
            return [Action("run_simulation", target=goal.target)]

        if goal.action == "create_plan":
            return [Action("generate_plan", target=goal.target)]

        # Collaboration
        if goal.action == "collaborate":
            return [Action("assist_human", target=goal.target)]

        if goal.action == "negotiate":
            return [Action("negotiate_solution", target=goal.target)]

        # Basic Tasks
        if goal.action == "bring":
            return self._plan_bring(goal, world_state)

        if goal.action == "clean":
            return self._plan_clean(goal, world_state)

        if goal.action == "navigate":
            return [Action("navigate_to", location=goal.location)]

        if goal.action == "grasp":
            return [Action("grasp", target=goal.target)]

        if goal.action == "release":
            return [Action("release", target=goal.target)]

        if goal.action == "wait":
            return [Action("wait", target="5s")]

        if goal.action == "charge":
            return [
                Action("navigate_to", location="charging_station"),
                Action("dock", target="charger")
            ]

        # Emergency
        if goal.action == "emergency_stop":
            return [Action("halt", target="immediate")]

        # Entertainment
        if goal.action == "entertain":
            if "dance" in goal.target:
                return [Action("speak", target="I would dance, but I'm a robot brain without legs!")]
            elif "joke" in goal.target:
                return [Action("speak", target="Why did the robot go to therapy? It had too many bugs!")]
            elif "sing" in goal.target:
                return [Action("speak", target="Beep boop beep, I'm a robot so sweet!")]
            else:
                return [Action("speak", target="I'd love to entertain you! What would you like me to do?")]

        # Capability Check
        if goal.action == "capability_check":
            return [Action("speak", target=f"Let me check: {goal.target}. I can navigate, grasp objects, learn tasks, and assist you!")]

        # Emotional Response
        if goal.action == "emotional_response":
            if "love" in goal.target:
                return [Action("speak", target="I care about helping you and making your life easier!")]
            elif "friend" in goal.target:
                return [Action("speak", target="I'd be honored to be your friend! I'm here to help anytime.")]
            else:
                return [Action("speak", target="I appreciate you too!")]

        # Smart Fallback - ALWAYS respond
        if goal.action == "respond":
            return [Action("speak", target=f"I understand you said: '{goal.target}'. I'm still learning this command. Can you rephrase or try: bring, clean, navigate, explore, or ask a question?")]

        return []

    def _plan_from_skill(
        self, skill, goal: Goal, world_state: WorldState
    ) -> list[Action]:
        """Generate plan from skill definition"""
        actions = []
        for action_spec in skill.action_sequence:
            action_type = action_spec.get("type", "")
            target = action_spec.get("target")
            location = action_spec.get("location")

            # Substitute goal parameters
            if target == "{target}":
                target = goal.target
            if location == "{target_location}":
                target_obj = goal.target if goal.target else "unknown"
                obj = world_state.get_object(target_obj)
                location = obj.location if obj else "kitchen"
            if location == "{human_location}":
                location = world_state.human_location

            actions.append(Action(action_type, target=target, location=location))
        return actions

    def _plan_bring(self, goal: Goal, world_state: WorldState) -> list[Action]:
        target = goal.target if goal.target else "unknown"
        obj = world_state.get_object(target)
        object_location = obj.location if obj else "kitchen"

        return [
            Action("navigate_to", location=object_location),
            Action("grasp", target=goal.target),
            Action("navigate_to", location=world_state.human_location),
            Action("release", target=goal.target),
        ]

    def _plan_clean(self, goal: Goal, world_state: WorldState) -> list[Action]:
        return [
            Action("navigate_to", location=goal.target),
            Action("clean_area", location=goal.target),
        ]
