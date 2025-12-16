# Decision Kernel Webots Adapter

Webots translation layer for Decision Kernel.

## What This Is

A **translation adapter** that bridges Decision Kernel to Webots simulator.

- Translates Webots world data to WorldState
- Translates Actions to Webots commands
- Passes Decision Kernel conformance tests

## What This Is Not

- Not a motion planner
- Not a perception system
- Not a physics simulator
- Not an autonomy framework

## Installation

```bash
pip install decision-kernel
pip install -e .
```

## Quick Demo

```bash
python demo.py
```

Expected output:
```
Decision Kernel - Webots Demo
==============================

[1/4] Creating Webots adapter...
[OK] Adapter created

[2/4] Sensing Webots world...
[OK] WorldState: 2 objects
  Robot at: start_position
  Objects: ['bottle', 'table']

[3/4] Processing intent...
  Intent: 'bring me the bottle'
[OK] Plan: 4 actions

[4/4] Executing in Webots...
  1. navigate_to(location=table)
  2. grasp(object=bottle)
  3. navigate_to(location=goal_position)
  4. release(object=bottle)

[WEBOTS] Would execute: navigate_to
  -> Set motor velocities to reach: table
  -> Use GPS/compass for navigation
[WEBOTS] Would execute: grasp
  -> Close gripper on: bottle
  -> Use touch sensors for feedback
[WEBOTS] Would execute: navigate_to
  -> Set motor velocities to reach: goal_position
  -> Use GPS/compass for navigation
[WEBOTS] Would execute: release
  -> Open gripper
  -> Release: bottle

[OK] Webots translation complete
  Success: True

Demo complete! Decision Kernel ran on Webots.
```

## Conformance

This adapter is **Decision Kernel Compatible**.

Verify:
```bash
python -m decision_kernel_conformance decision_kernel_webots.adapter.WebotsAdapter
```

Expected: 4/4 tests passed

## Usage with Real Webots

```python
from controller import Robot
from decision_kernel_webots.adapter import WebotsAdapter
from brain.kernel import RobotBrainKernel

# In Webots controller
robot = Robot()
adapter = WebotsAdapter(robot=robot)
kernel = RobotBrainKernel(adapter=adapter)

# Sense-Plan-Execute loop
while robot.step(timestep) != -1:
    world_state = adapter.sense()
    plan = kernel.process(intent, world_state)
    report = adapter.execute(plan)
```

## Supported Actions

- `navigate_to` - Navigate to location
- `grasp` - Grasp object
- `release` - Release object

## Scope

This adapter:
- ✓ Implements Adapter contract
- ✓ Translates data formats
- ✓ Logs intended actions
- ✗ Does NOT control motors directly
- ✗ Does NOT implement planning
- ✗ Does NOT run physics

## Architecture

```
Decision Kernel → WebotsAdapter → Webots API
   (planning)      (translation)    (execution)
```

The adapter is a **thin translation layer**.

## License

Apache License 2.0
