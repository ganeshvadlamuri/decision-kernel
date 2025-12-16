"""Demonstration of skill system usage"""

from brain.kernel import RobotBrainKernel
from brain.skills.builtin import create_bring_water_skill
from brain.skills.registry import SkillRegistry
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def main():
    # Create skill registry and register built-in skill
    registry = SkillRegistry()
    registry.register(create_bring_water_skill())

    # Create kernel with skill support
    kernel = RobotBrainKernel(skill_registry=registry)

    # Create world state
    world = WorldState(
        objects=[
            WorldObject("water", "kitchen", "liquid"),
            WorldObject("cup", "kitchen", "container"),
        ],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room", "bedroom"],
    )

    # Process command using skill
    print("Using skill-based planning:")
    plan = kernel.process("bring me water", world)

    print("\nGenerated plan:")
    for i, action in enumerate(plan, 1):
        print(f"  {i}. {action}")

    print(f"\nRegistered skills: {registry.list()}")


if __name__ == "__main__":
    main()
