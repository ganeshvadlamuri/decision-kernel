import sys

from adapters.mock.mock_robot import MockRobot
from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def create_mock_world() -> WorldState:
    """Create a simple mock world state"""
    return WorldState(
        objects=[
            WorldObject("cup", "kitchen", "container"),
            WorldObject("water", "kitchen", "liquid"),
            WorldObject("book", "living room", "item"),
        ],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room", "bedroom", "bathroom"]
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli/run.py <command>")
        print('Example: python cli/run.py "bring me water"')
        sys.exit(1)

    human_input = " ".join(sys.argv[1:])

    kernel = RobotBrainKernel()
    world_state = create_mock_world()

    print(f"\nInput: {human_input}")

    try:
        plan = kernel.process(human_input, world_state)

        print("\nPlan:")
        for i, action in enumerate(plan, 1):
            print(f"  {i}. {action}")

        print("\nSafety: PASS")

        robot = MockRobot()
        robot.execute(plan)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
