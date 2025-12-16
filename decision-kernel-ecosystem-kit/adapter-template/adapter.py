"""Decision Kernel adapter template"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class MyAdapter:
    """Adapter for [YOUR HARDWARE/SIMULATION]"""

    def __init__(self):
        """Initialize hardware connections"""
        # TODO: Initialize your hardware/simulation
        pass

    def sense(self) -> WorldState:
        """
        Read sensors and construct WorldState

        Returns:
            WorldState with current environment state
        """
        # TODO: Read your sensors
        # TODO: Detect objects
        # TODO: Get robot position
        # TODO: Build WorldState

        return WorldState(
            objects=[
                WorldObject("example_object", "example_location", "graspable"),
            ],
            robot_location="base",
            human_location="home",
            locations=["base", "home", "example_location"],
            timestamp=time.time(),
            frame_id="world",
            relations={},
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Execute action plan

        Args:
            plan: List of actions to execute

        Returns:
            ExecutionReport with execution results
        """
        report = ExecutionReport(success=True, message="Execution complete")

        for i, action in enumerate(plan):
            # TODO: Execute action on your hardware
            print(f"Executing: {action}")

            # Example: Handle different action types
            if action.action_type == "navigate_to":
                # TODO: Send navigation command
                pass

            elif action.action_type == "grasp":
                # TODO: Send grasp command
                pass

            elif action.action_type == "release":
                # TODO: Send release command
                pass

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
        Report adapter capabilities

        Returns:
            Dictionary with supported actions and metadata
        """
        return {
            "supported_actions": [
                "navigate_to",
                "grasp",
                "release",
                # TODO: Add your supported actions
            ],
            "sensing": ["camera", "lidar"],  # TODO: Your sensors
            "hardware": "my_robot",  # TODO: Your hardware name
            "version": "1.0",
        }
