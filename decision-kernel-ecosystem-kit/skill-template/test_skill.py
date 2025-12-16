"""Test skill"""

from skill import create_my_skill

from brain.kernel import RobotBrainKernel
from brain.skills.registry import SkillRegistry
from brain.world.state import WorldState


def test_skill():
    """Test skill integration"""
    # Register skill
    registry = SkillRegistry()
    registry.register(create_my_skill())

    # Create kernel with skill
    kernel = RobotBrainKernel(skill_registry=registry)

    # Test planning
    world_state = WorldState(
        objects=[],
        robot_location="base",
        human_location="home",
        locations=["base", "home"],
    )

    # TODO: Update with your intent
    plan = kernel.process("your intent here", world_state)

    assert len(plan) > 0, "Skill should generate plan"
    print(f"[OK] Skill generated {len(plan)} actions")


if __name__ == "__main__":
    test_skill()
