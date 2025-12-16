# Adoption Guide

How to integrate Decision Kernel into your robot stack.

## Overview

Decision Kernel sits between human intent and hardware execution:

```
Human → Decision Kernel → Your Hardware
         (intent → plan)   (execution)
```

## Integration Steps

### 1. Install Decision Kernel

```bash
pip install decision-kernel
```

### 2. Create an Adapter

Your adapter translates between Decision Kernel and your hardware:

```python
from brain.world.state import WorldState
from brain.planner.actions import Action
from brain.execution.report import ExecutionReport

class MyRobotAdapter:
    def sense(self) -> WorldState:
        """Read your sensors, return WorldState"""
        # Read sensors
        # Detect objects
        # Build WorldState
        pass
    
    def execute(self, plan: list[Action]) -> ExecutionReport:
        """Execute actions on your hardware"""
        # Translate actions to hardware commands
        # Execute
        # Return report
        pass
    
    def capabilities(self) -> dict:
        """Report what your robot can do"""
        return {
            "supported_actions": ["navigate_to", "grasp"],
            "hardware": "my_robot",
            "version": "1.0"
        }
```

See [Adapter Contract](adapter_contract.md) for full specification.

### 3. Use the Kernel

```python
from brain.kernel import RobotBrainKernel

adapter = MyRobotAdapter()
kernel = RobotBrainKernel(adapter=adapter)

# Sense → Plan → Execute
world_state = adapter.sense()
plan = kernel.process("bring me water", world_state)
report = adapter.execute(plan)
```

### 4. Verify Conformance

```bash
python -m decision_kernel_conformance my_adapter.MyRobotAdapter
```

Must pass 4/4 tests to be Decision Kernel Compatible.

## Architecture Patterns

### Pattern 1: Direct Integration

```
Your Code → Decision Kernel → Your Hardware
```

Best for: New projects, simple stacks

### Pattern 2: ROS2 Integration

```
Your Code → Decision Kernel → ROS2 Adapter → ROS2 → Hardware
```

Best for: Existing ROS2 systems

See [decision-kernel-ros2](../decision-kernel-ros2/) for reference.

### Pattern 3: Hybrid

```
Your Code → Decision Kernel → Custom Adapter → [ROS2/Other] → Hardware
```

Best for: Complex systems with multiple middleware layers

## Common Integration Points

### With Motion Planners

Decision Kernel generates high-level actions (`navigate_to`). Your adapter calls your motion planner:

```python
def execute(self, plan):
    for action in plan:
        if action.action_type == "navigate_to":
            # Call your motion planner
            trajectory = motion_planner.plan(action.location)
            robot.execute_trajectory(trajectory)
```

### With Perception Systems

Your adapter reads perception outputs and builds WorldState:

```python
def sense(self):
    objects = perception_system.detect_objects()
    robot_pose = localization.get_pose()
    
    return WorldState(
        objects=[WorldObject(o.name, o.location, o.type) for o in objects],
        robot_location=robot_pose,
        ...
    )
```

### With Safety Systems

Decision Kernel has built-in safety checks. Add hardware-specific checks in your adapter:

```python
def execute(self, plan):
    # Kernel already validated plan
    # Add hardware-specific checks
    if not self.robot.is_safe():
        raise SafetyError("Hardware safety check failed")
    
    # Execute
    ...
```

## Best Practices

1. **Keep adapter thin**: Translate, don't implement autonomy
2. **Use existing tools**: Call your motion planner, perception, etc.
3. **Validate conformance**: Run conformance tests regularly
4. **Handle errors**: Return proper ExecutionReport status
5. **Document capabilities**: Clearly list supported actions

## Examples

- [ROS2 Demo](../demos/ros2_hello_world/) - End-to-end example
- [Mock Adapter](../adapters/mock/) - Simple reference implementation
- [ROS2 Adapter](../decision-kernel-ros2/) - Production-ready ROS2 integration

## Getting Help

- Check [documentation](../docs/)
- Review [examples](../examples/)
- Open an issue on GitHub
- See [ecosystem kit](../decision-kernel-ecosystem-kit/) for templates

## Next Steps

1. Create your adapter using [ecosystem kit](../decision-kernel-ecosystem-kit/)
2. Test with conformance runner
3. Integrate into your robot
4. Share with community (optional)
