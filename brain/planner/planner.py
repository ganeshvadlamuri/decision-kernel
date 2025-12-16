
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
        if goal.action == "bring":
            return self._plan_bring(goal, world_state)

        if goal.action == "clean":
            return self._plan_clean(goal, world_state)

        if goal.action == "navigate":
            return [Action("navigate_to", location=goal.location)]

        if goal.action == "grasp":
            return [Action("grasp", target=goal.target)]

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
