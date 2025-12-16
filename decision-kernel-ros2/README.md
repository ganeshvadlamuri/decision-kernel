# Decision Kernel ROS2 Adapter

ROS2 adapter implementing the Decision Kernel Adapter contract.

## Scope

This adapter is a **translation layer** between Decision Kernel and ROS2.

### What It Does

- Translates ROS2 topics to WorldState
- Translates Actions to ROS2 messages
- Implements full Adapter contract
- Passes conformance tests

### What It Does NOT Do

- Motion planning (use MoveIt2)
- Trajectory generation (use nav2)
- Hardware control (use ros2_control)
- Perception algorithms (use your perception stack)
- Autonomy (that's the kernel's job)

## Philosophy

Decision Kernel provides decision-making.
ROS2 provides execution infrastructure.
This adapter bridges them without duplicating functionality.

## Installation

```bash
# Install Decision Kernel
cd ../decision-kernel
pip install -e .

# Install ROS2 adapter
cd ../decision-kernel-ros2
pip install -e .
```

## Usage

### Basic Usage

```python
from decision_kernel_ros2.adapter import ROS2Adapter
from brain.kernel import RobotBrainKernel

# Create adapter
adapter = ROS2Adapter()

# Use with kernel
kernel = RobotBrainKernel(adapter=adapter)
world = adapter.sense()
plan = kernel.process("bring me water", world)
report = adapter.execute(plan)
```

### With ROS2 Node (Production)

```python
import rclpy
from decision_kernel_ros2.adapter import ROS2Adapter

rclpy.init()
adapter = ROS2Adapter()

# Adapter subscribes to:
# - /tf
# - /odom
# - /joint_states

# Adapter publishes to:
# - /cmd_vel
# - /gripper/command
# - Action servers
```

## Conformance

Verify adapter passes Decision Kernel conformance:

```bash
cd ../decision-kernel
python -m decision_kernel_conformance decision_kernel_ros2.adapter.ROS2Adapter
```

Expected output:
```
[PASS]: Method presence
[PASS]: sense() contract
[PASS]: execute() contract
[PASS]: capabilities() contract
[PASS] Adapter is CONFORMANT
```

## Architecture

```
┌─────────────────┐
│ Decision Kernel │  ← Decision-making
└────────┬────────┘
         │
    ┌────▼────┐
    │ Adapter │  ← Translation only
    └────┬────┘
         │
    ┌────▼────┐
    │  ROS2   │  ← Execution infrastructure
    └─────────┘
```

## Integration Points

### Input (sense)
- `/tf` → robot/object locations
- `/odom` → robot pose
- `/camera/objects` → detected objects

### Output (execute)
- `/cmd_vel` → navigation commands
- `/gripper/command` → manipulation
- Action servers → complex behaviors

## Non-Goals

This adapter explicitly does NOT:
- Replace MoveIt2
- Replace nav2
- Replace ros2_control
- Implement SLAM
- Implement perception
- Control hardware directly

## Dependencies

**Required:**
- decision-kernel >= 0.5.0

**Optional (for ROS2 integration):**
- rclpy
- geometry_msgs
- nav_msgs
- sensor_msgs

## Development

```bash
# Run conformance
python -m decision_kernel_conformance decision_kernel_ros2.adapter.ROS2Adapter

# Run tests
pytest tests/
```

## License

Apache License 2.0 (same as Decision Kernel)

## Status

**Production Ready** - Translation layer only

For hardware control, integrate with:
- MoveIt2 (manipulation)
- nav2 (navigation)
- ros2_control (low-level control)
