"""Minimal adapter template implementing the Adapter protocol"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class MyAdapter:
    """Template adapter - replace with your hardware/simulation integration"""

    def sense(self) -> WorldState:
        """
        Query your sensors/simulation and return current world state

        Replace this with your actual sensing logic:
        - Read sensor data
        - Query simulation state
        - Construct WorldState representation
        """
        return WorldState(
            objects=[
                WorldObject("example_object", "example_location", "example_type"),
            ],
            robot_location="home",
            human_location="home",
            locations=["home", "kitchen", "bedroom"],
            timestamp=time.time(),
            frame_id="world",
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Execute action plan on your hardware/simulation

        Replace this with your actual execution logic:
        - Send commands to hardware
        - Execute in simulation
        - Handle errors gracefully
        """
        report = ExecutionReport(success=True, message="Execution complete")

        for i, action in enumerate(plan):
            # TODO: Replace with actual execution
            print(f"Executing: {action}")

            # Record result
            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Executed {action.action_type}",
                duration=0.1,
            )
            report.add_result(result)

        return report

    def capabilities(self) -> dict:
        """
        Report what your adapter can do

        Update this to match your hardware capabilities
        """
        return {
            "supported_actions": [
                "navigate_to",
                "grasp",
                "release",
                # Add your supported actions here
            ],
            "sensing": ["camera", "lidar"],  # Update with your sensors
            "hardware": "my_robot",  # Update with your hardware name
            "version": "1.0",
        }
