# ROS2 Hello World Demo

End-to-end demonstration of Decision Kernel with ROS2 adapter.

## What This Shows

1. **Simulated ROS2 topics** (`/tf`, `/odom`) without requiring ROS2 installation
2. **ROS2 adapter** translating topics to WorldState
3. **Kernel processing** intent → plan → safety check
4. **Execution** with simulated ROS2 publishers

## Run Demo

```bash
# From repository root
python -m demos.ros2_hello_world.run
```

Or using Make:
```bash
make demo-ros2
```

## Expected Output

```
Decision Kernel - ROS2 Hello World Demo
========================================

[1/4] Creating ROS2 adapter...
✓ Adapter created

[2/4] Sensing world state from ROS2 topics...
✓ WorldState: 2 objects, 3 locations
  Robot at: base_link
  Objects: ['cup', 'table']

[3/4] Processing intent through kernel...
  Intent: 'bring me the cup'
✓ Plan generated: 4 actions
  Safety: PASS

[4/4] Executing plan...
  1. navigate_to(location=kitchen)
  2. grasp(object=cup)
  3. navigate_to(location=living_room)
  4. release(object=cup)

[DEMO] Executing: navigate_to(location=kitchen)
[SIM] /cmd_vel: linear=0.5, angular=0.0
[SIM] /cmd_vel: linear=0.0, angular=0.0

[DEMO] Executing: grasp(object=cup)
[SIM] /gripper/command: position=0.0

[DEMO] Executing: navigate_to(location=living_room)
[SIM] /cmd_vel: linear=0.5, angular=0.0
[SIM] /cmd_vel: linear=0.0, angular=0.0

[DEMO] Executing: release(object=cup)
[SIM] /gripper/command: position=1.0

✓ Execution: Demo execution complete
  Success: True
  Actions completed: 4

Demo complete! Decision Kernel ran end-to-end with ROS2.
```

## What's Happening

- **No ROS2 required**: Uses simulated topics for demo purposes
- **Real adapter pattern**: Shows how to integrate with ROS2
- **Full kernel pipeline**: Intent → WorldState → Planning → Safety → Execution
- **Capability checking**: Kernel validates actions against adapter capabilities

## Next Steps

For real ROS2 integration, see [decision-kernel-ros2](../../decision-kernel-ros2/) adapter.
