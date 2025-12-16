"""Webots adapter for Decision Kernel - Translation layer only"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class WebotsAdapter:
    """
    Webots adapter implementing Decision Kernel contract

    SCOPE:
    - Translates Webots world data to WorldState
    - Translates Actions to Webots commands
    - Does NOT control robot directly
    - Does NOT implement autonomy

    NON-GOALS:
    - Motion planning
    - Trajectory generation
    - Physics simulation
    - Perception algorithms
    """

    def __init__(self, robot=None):
        """
        Initialize Webots adapter

        Args:
            robot: Webots Robot instance (optional, for real Webots integration)

        In production:
        - Initialize Webots Robot instance
        - Get device references (motors, sensors)
        - Set up supervisor if needed

        For demo: Uses mocked Webots API
        """
        self.robot = robot
        self.world_frame = "world"
        self.kernel_version = "0.7.0"

    def sense(self) -> WorldState:
        """
        Query Webots world and construct WorldState

        In production:
        - Read robot position from GPS/supervisor
        - Read sensor data (distance, camera, lidar)
        - Query world objects via supervisor
        - Convert to WorldState format

        Returns:
            WorldState with Webots data translated to kernel format
        """
        # Simulated Webots world data
        # In production: world_data = self._read_webots_world()

        return WorldState(
            objects=[
                WorldObject("bottle", "table", "graspable"),
                WorldObject("table", "room", "surface"),
            ],
            robot_location="start_position",
            human_location="goal_position",
            locations=["start_position", "table", "room", "goal_position"],
            timestamp=time.time(),
            frame_id=self.world_frame,
            relations={"bottle": {"on": "table"}},
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Translate actions to Webots commands

        DOES NOT MOVE ROBOT

        In production:
        - Set motor velocities for navigation
        - Control gripper motors for manipulation
        - Use supervisor for visualization
        - Log to Webots console

        For demo: Logs intended actions

        Args:
            plan: List of actions to translate

        Returns:
            ExecutionReport with translation results
        """
        report = ExecutionReport(success=True, message="Webots translation complete")

        for i, action in enumerate(plan):
            # Log what would be executed in Webots
            print(f"[WEBOTS] Would execute: {action.action_type}")

            if action.action_type == "navigate_to":
                print(f"  -> Set motor velocities to reach: {action.location}")
                print("  -> Use GPS/compass for navigation")

            elif action.action_type == "grasp":
                print(f"  -> Close gripper on: {action.target}")
                print("  -> Use touch sensors for feedback")

            elif action.action_type == "release":
                print("  -> Open gripper")
                print(f"  -> Release: {action.target}")

            # Record successful translation
            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Translated {action.action_type} to Webots",
                duration=0.01,
            )
            report.add_result(result)

        return report

    def capabilities(self) -> dict:
        """
        Report Webots adapter capabilities

        Returns:
            Dictionary with supported actions and metadata
        """
        return {
            "supported_actions": [
                "navigate_to",
                "grasp",
                "release",
            ],
            "sensing": ["gps", "distance_sensor", "camera"],
            "hardware": "webots",
            "version": "1.0",
            "kernel_version": self.kernel_version,
            "simulator": "webots",
        }
