"""Tests for skill system"""

from brain.intent.schema import Goal
from brain.planner.planner import Planner
from brain.skills.builtin import create_bring_water_skill
from brain.skills.registry import SkillRegistry
from brain.skills.skill import Skill
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def test_skill_creation():
    """Skills can be created with required fields"""
    skill = Skill(
        name="test",
        description="Test skill",
        inputs={"param": "value"},
        preconditions=["condition"],
        effects=["effect"],
        action_sequence=[{"type": "action"}],
    )
    assert skill.name == "test"
    assert skill.description == "Test skill"


def test_skill_registry_register():
    """Registry can register skills"""
    registry = SkillRegistry()
    skill = Skill(name="test", description="Test")

    registry.register(skill)
    assert "test" in registry.list()


def test_skill_registry_get():
    """Registry can retrieve registered skills"""
    registry = SkillRegistry()
    skill = Skill(name="test", description="Test")

    registry.register(skill)
    retrieved = registry.get("test")

    assert retrieved is not None
    assert retrieved.name == "test"


def test_skill_registry_get_missing():
    """Registry returns None for unregistered skills"""
    registry = SkillRegistry()
    assert registry.get("nonexistent") is None


def test_planner_uses_skill_when_registered():
    """Planner uses skill plan when skill is registered"""
    registry = SkillRegistry()
    skill = create_bring_water_skill()
    registry.register(skill)

    planner = Planner(skill_registry=registry)
    goal = Goal(action="bring", target="water")
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        human_location="living room",
    )

    plan = planner.plan(goal, world)

    assert len(plan) == 4
    assert plan[0].action_type == "navigate_to"
    assert plan[0].location == "kitchen"
    assert plan[1].action_type == "grasp"
    assert plan[1].target == "water"
    assert plan[2].action_type == "navigate_to"
    assert plan[2].location == "living room"
    assert plan[3].action_type == "release"


def test_planner_fallback_without_skill():
    """Planner falls back to naive planning without skill registry"""
    planner = Planner(skill_registry=None)
    goal = Goal(action="bring", target="water")
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        human_location="living room",
    )

    plan = planner.plan(goal, world)

    # Should still produce valid plan via fallback
    assert len(plan) == 4
    assert plan[0].action_type == "navigate_to"


def test_planner_fallback_for_unregistered_action():
    """Planner falls back for actions without registered skills"""
    registry = SkillRegistry()
    planner = Planner(skill_registry=registry)

    goal = Goal(action="navigate", location="kitchen")
    world = WorldState()

    plan = planner.plan(goal, world)

    # Should use naive planning fallback
    assert len(plan) == 1
    assert plan[0].action_type == "navigate_to"
    assert plan[0].location == "kitchen"


def test_builtin_bring_skill():
    """Built-in bring skill produces correct action sequence"""
    skill = create_bring_water_skill()

    assert skill.name == "bring"
    assert len(skill.action_sequence) == 4
    assert skill.action_sequence[0]["type"] == "navigate_to"
    assert skill.action_sequence[1]["type"] == "grasp"
