# Decision Kernel PyBullet Adapter

PyBullet physics simulation adapter for Decision Kernel.

## What This Is

A **translation adapter** that bridges Decision Kernel to PyBullet physics simulator.

- Translates PyBullet simulation data to WorldState
- Translates Actions to PyBullet commands
- Passes Decision Kernel conformance tests

## What This Is Not

- Not a physics engine
- Not a motion planner
- Not a perception system
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

Runtime: <1 minute

## Conformance

This adapter is **Decision Kernel Compatible**.

Verify:
```bash
python -m decision_kernel_conformance decision_kernel_pybullet.adapter.PyBulletAdapter
```

Expected: 4/4 tests passed

## Supported Actions

- `navigate_to` - Navigate to location
- `grasp` - Grasp object
- `release` - Release object

## License

Apache License 2.0
