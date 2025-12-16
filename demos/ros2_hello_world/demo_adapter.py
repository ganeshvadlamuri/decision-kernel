"""Demo ROS2 adapter using simulated robot"""

import time

from brain.execution.report import ActionResult, ExecutionReport, ExecutionStatus
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState

from .simulated_robot import SimulatedROS2Robot


class DemoROS2Adapter:
    """ROS2 adapter using simulated robot for demo purposes"""

    def __init__(self):
        self.robot = SimulatedROS2Robot()

    def sense(self) -> WorldState:
        """Read simulated ROS2 topics and build WorldState"""
        tf_data = self.robot.get_tf()

        # Extract locations from transforms
        locations = [tf.child_frame_id for tf in tf_data]

        return WorldState(
            objects=[
                WorldObject("cup", "kitchen", "graspable"),
                WorldObject("table", "kitchen", "surface"),
            ],
            robot_location="base_link",
            human_location="living_room",
            locations=locations + ["living_room"],
            timestamp=time.time(),
            frame_id="world",
            relations={"cup": {"on": "table"}},
        )

    def execute(self, plan: list[Action]) -> ExecutionReport:
        """Execute plan using simulated ROS2 publishers"""
        report = ExecutionReport(success=True, message="Demo execution complete")

        for i, action in enumerate(plan):
            print(f"\n[DEMO] Executing: {action}")

            if action.action_type == "navigate_to":
                self.robot.publish_cmd_vel(linear=0.5, angular=0.0)
                time.sleep(0.1)
                self.robot.publish_cmd_vel(linear=0.0, angular=0.0)

            elif action.action_type == "grasp":
                self.robot.publish_gripper_command(position=0.0)

            elif action.action_type == "release":
                self.robot.publish_gripper_command(position=1.0)

            result = ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS,
                message=f"Executed {action.action_type}",
                duration=0.1,
            )
            report.add_result(result)

        return report

    def capabilities(self) -> dict:
        """Report adapter capabilities"""
        return {
            "supported_actions": ["navigate_to", "grasp", "release"],
            "sensing": ["tf", "odom"],
            "hardware": "simulated_ros2",
            "version": "1.0",
        }
