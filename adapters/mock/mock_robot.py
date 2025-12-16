import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class MockRobot:
    """Mock robot implementing Adapter contract"""

    def sense(self) -> WorldState:
        """Return mock world state"""
        return WorldState(
            objects=[
                WorldObject("cup", "kitchen", "container"),
                WorldObject("water", "kitchen", "liquid"),
            ],
            robot_location="living_room",
            human_location="living_room",
            locations=["kitchen", "living_room", "bedroom"],
            timestamp=time.time(),
            frame_id="world",
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """Execute plan by printing actions"""
        print("\n=== Executing Plan ===")
        report = ExecutionReport(success=True, message="Mock execution complete")

        for i, action in enumerate(plan):
            print(f"  {i + 1}. {action}")
            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Executed {action.action_type}",
                duration=0.1,
            )
            report.add_result(result)

        print("=== Execution Complete ===\n")
        return report

    def capabilities(self) -> dict:
        """Report mock adapter capabilities"""
        return {
            "supported_actions": ["navigate_to", "grasp", "release", "clean_area"],
            "sensing": ["mock"],
            "hardware": "mock",
            "version": "1.0",
        }
