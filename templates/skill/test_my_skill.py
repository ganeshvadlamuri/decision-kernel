"""Example test for custom skill"""

from my_skill import create_my_skill

from brain.intent.schema import Goal
from brain.planner.planner import Planner
from brain.skills.registry import SkillRegistry
from brain.world.state import WorldState


def test_skill_creation():
    """Skill can be created"""
    skill = create_my_skill()
    assert skill.name == "my_skill"
    assert len(skill.action_sequence) > 0


def test_skill_registration():
    """Skill can be registered"""
    registry = SkillRegistry()
    skill = create_my_skill()
    registry.register(skill)
    assert "my_skill" in registry.list()


def test_skill_planning():
    """Planner uses skill when registered"""
    registry = SkillRegistry()
    registry.register(create_my_skill())

    planner = Planner(skill_registry=registry)
    goal = Goal(action="my_skill", target="object")
    world = WorldState()

    plan = planner.plan(goal, world)
    assert len(plan) > 0


if __name__ == "__main__":
    test_skill_creation()
    test_skill_registration()
    test_skill_planning()
    print("All tests passed!")
