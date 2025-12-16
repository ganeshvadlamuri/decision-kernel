"""PyBullet adapter for Decision Kernel - Translation layer only"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class PyBulletAdapter:
    """
    PyBullet adapter implementing Decision Kernel contract

    SCOPE:
    - Translates PyBullet simulation data to WorldState
    - Translates Actions to PyBullet commands
    - Does NOT control physics directly
    - Does NOT implement autonomy

    NON-GOALS:
    - Physics simulation
    - Collision detection
    - Trajectory planning
    - Perception algorithms
    """

    def __init__(self, client=None):
        """
        Initialize PyBullet adapter

        Args:
            client: PyBullet physics client (optional)

        In production:
        - Initialize PyBullet physics client
        - Load robot URDF
        - Set up simulation parameters

        For demo: Uses mocked PyBullet API
        """
        self.client = client
        self.world_frame = "world"
        self.kernel_version = "0.9.0"

    def sense(self) -> WorldState:
        """
        Query PyBullet simulation and construct WorldState

        In production:
        - Read body positions from PyBullet
        - Query object states
        - Get robot joint states
        - Convert to WorldState format

        Returns:
            WorldState with PyBullet data translated to kernel format
        """
        # Simulated PyBullet world data
        # In production: positions = p.getBasePositionAndOrientation(body_id)

        return WorldState(
            objects=[
                WorldObject("cube", "table", "graspable"),
                WorldObject("table", "room", "surface"),
            ],
            robot_location="start_position",
            human_location="goal_position",
            locations=["start_position", "table", "room", "goal_position"],
            timestamp=time.time(),
            frame_id=self.world_frame,
            relations={"cube": {"on": "table"}},
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """
        Translate actions to PyBullet commands

        DOES NOT CONTROL PHYSICS

        In production:
        - Set joint positions/velocities
        - Apply forces/torques
        - Step simulation
        - Monitor execution

        For demo: Logs intended actions

        Args:
            plan: List of actions to translate

        Returns:
            ExecutionReport with translation results
        """
        report = ExecutionReport(success=True, message="PyBullet translation complete")

        for i, action in enumerate(plan):
            # Log what would be executed in PyBullet
            print(f"[PYBULLET] Would execute: {action.action_type}")

            if action.action_type == "navigate_to":
                print(f"  -> Set base velocity to reach: {action.location}")
                print("  -> Step simulation until target reached")

            elif action.action_type == "grasp":
                print(f"  -> Close gripper on: {action.target}")
                print("  -> Apply gripper force constraints")

            elif action.action_type == "release":
                print("  -> Open gripper")
                print(f"  -> Release: {action.target}")

            # Record successful translation
            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Translated {action.action_type} to PyBullet",
                duration=0.01,
            )
            report.add_result(result)

        return report

    def capabilities(self) -> dict:
        """
        Report PyBullet adapter capabilities

        Returns:
            Dictionary with supported actions and metadata
        """
        return {
            "supported_actions": [
                "navigate_to",
                "grasp",
                "release",
            ],
            "sensing": ["position", "orientation", "joint_states"],
            "hardware": "pybullet",
            "version": "1.0",
            "kernel_version": self.kernel_version,
            "simulator": "pybullet",
        }
