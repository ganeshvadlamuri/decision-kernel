"""ROS2 adapter for Decision Kernel - Translation layer only"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class ROS2Adapter:
    """
    ROS2 adapter implementing Decision Kernel contract

    SCOPE:
    - Translates ROS2 data to WorldState
    - Translates Actions to ROS2 messages
    - Does NOT control hardware directly
    - Does NOT implement autonomy

    NON-GOALS:
    - Motion planning
    - Trajectory generation
    - Hardware control
    - Perception algorithms
    """

    def __init__(self):
        """
        Initialize ROS2 adapter

        In production:
        - Initialize ROS2 node
        - Subscribe to /tf, /odom, /joint_states
        - Create action publishers

        For now: Simulated placeholders
        """
        self.robot_frame = "base_link"
        self.world_frame = "world"

    def sense(self) -> WorldState:
        """
        Query ROS2 topics and construct WorldState

        In production:
        - Read /tf for transforms
        - Read /odom for robot pose
        - Read sensor topics for objects
        - Convert to WorldState format

        Returns:
            WorldState with ROS2 data translated to kernel format
        """
        # Simulated ROS2 data translation
        # In production: ros2_data = self._read_topics()

        return WorldState(
            objects=[
                WorldObject("detected_object", "table", "unknown"),
            ],
            robot_location="base_link",
            human_location="operator_station",
            locations=["base_link", "table", "operator_station"],
            timestamp=time.time(),
            frame_id=self.world_frame,
            relations={"detected_object": {"on": "table"}},
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Translate actions to ROS2 messages

        DOES NOT MOVE HARDWARE

        In production:
        - Publish to /cmd_vel for navigation
        - Publish to /gripper/command for manipulation
        - Publish to action servers

        For now: Logs intended actions

        Args:
            plan: List of actions to translate

        Returns:
            ExecutionReport with translation results
        """
        report = ExecutionReport(success=True, message="ROS2 translation complete")

        for i, action in enumerate(plan):
            # Log what would be published
            print(f"[ROS2] Would publish: {action.action_type}")

            if action.action_type == "navigate_to":
                print("  -> Topic: /cmd_vel")
                print(f"  -> Target: {action.location}")

            elif action.action_type == "grasp":
                print("  -> Topic: /gripper/command")
                print(f"  -> Target: {action.target}")

            elif action.action_type == "release":
                print("  -> Topic: /gripper/command")
                print("  -> Action: open")

            # Record successful translation
            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Translated {action.action_type} to ROS2",
                duration=0.01,
            )
            report.add_result(result)

        return report

    def capabilities(self) -> dict:
        """
        Report ROS2 adapter capabilities

        Returns:
            Dictionary with supported actions and hardware info
        """
        return {
            "supported_actions": [
                "navigate_to",
                "grasp",
                "release",
            ],
            "sensing": ["tf", "odom"],
            "hardware": "ros2",
            "version": "1.0",
            "ros_distro": "humble",  # ROS2-specific metadata
            "middleware": "dds",
        }
