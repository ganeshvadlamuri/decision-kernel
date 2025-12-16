# Decision Kernel

![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![MyPy](https://img.shields.io/badge/type%20check-mypy-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

A minimal, hardware-agnostic robot brain kernel for autonomous decision-making.

> **Decision Kernel is infrastructure, not a product.**  
> It is vendor-neutral, hardware-agnostic, and community-driven.

## v1.0 Candidate Status

**Decision Kernel is feature-complete and frozen.**

Core, specifications, and contracts are immutable. v1.0 will be released upon adoption milestones (education, research, industry). Stability guarantees are active now.

**What remains**: External validation, not technical work.

**See**: [v1.0 Candidate](docs/v1_candidate.md) | [Roadmap](docs/roadmap.md)

## v1.0 Stability Commitment

Decision Kernel is entering long-term stable phase:

- **Core interfaces will not change** - Adapter contract frozen at v1.0
- **10+ year compatibility** - Code written for v1.0 works on v1.x forever
- **No breaking changes** - v1.x series maintains backward compatibility
- **Ecosystem extensions encouraged** - Innovation happens in adapters, skills, tools
- **Kernel changes intentionally rare** - Stability over features

**What this means for you**:
- Safe to build long-lived systems on Decision Kernel
- Safe to teach in university courses (materials remain valid)
- Safe to cite in research papers (reproducibility guaranteed)
- Safe to invest engineering time (no API churn)

**See**: [v1.0 Definition](docs/v1_definition.md) | [Freeze Policy](docs/v1_freeze.md)

## What It Is

Decision Kernel is a lightweight orchestration layer that processes human intent, evaluates world state, generates action plans, validates safety constraints, and maintains execution memory. It provides a clean separation between decision logic and hardware execution.

## What It Is Not

- Not a motion planner
- Not a perception system
- Not a hardware driver
- Not a ROS package (though it can integrate with ROS via adapters)
- Not an AI/ML framework

## Architecture

```
Intent → World State → Planning → Safety Check → Memory → Execution
```

The kernel orchestrates five core modules:

- **Intent**: Parse human commands into structured goals
- **World**: Maintain representation of environment state
- **Planner**: Generate action sequences to achieve goals
- **Safety**: Validate plans against constraints
- **Memory**: Store execution history

## Philosophy

This is infrastructure, not a product. The kernel makes no assumptions about:

- Hardware platform
- Sensor modalities
- Actuator types
- Communication protocols

Adapters bridge the kernel to real systems.

## Installation

```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
python cli/run.py "bring me water"
```

### Using Skills (v0.2+)

```python
from brain.kernel import RobotBrainKernel
from brain.skills.registry import SkillRegistry
from brain.skills.builtin import create_bring_water_skill

# Register skills
registry = SkillRegistry()
registry.register(create_bring_water_skill())

# Create kernel with skills
kernel = RobotBrainKernel(skill_registry=registry)
```

See [Skill Specification](docs/skill_spec.md) for details.

## Example Output

```
Intent: bring water to human
Plan:
  1. navigate_to(location=kitchen)
  2. grasp(object=cup)
  3. navigate_to(location=human)
  4. release(object=cup)
Safety: PASS
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Lint and format
ruff check . --fix

# Type check
mypy brain/ cli/ adapters/ --ignore-missing-imports
```

## Testing

```bash
pytest tests/ -v
```

All tests are fast, deterministic, and require no hardware.

## Quick Start

### Try the Demo (v0.6+)

```bash
# Run end-to-end ROS2 demo (no ROS2 required)
python -m demos.ros2_hello_world.run

# Or using Make
make demo-ros2
```

See [ROS2 Demo](demos/ros2_hello_world/) for details.

### Create an Adapter (v0.4+)

```bash
# Use ecosystem kit template
cp -r decision-kernel-ecosystem-kit/adapter-template my_adapter
cd my_adapter
# Edit adapter.py with your hardware logic
python -m decision_kernel_conformance adapter.MyAdapter
```

### Create a Skill (v0.4+)

```bash
# Use ecosystem kit template
cp -r decision-kernel-ecosystem-kit/skill-template my_skill
cd my_skill
# Edit skill.py with your behavior
python test_skill.py
```

## Decision Kernel Compatible

An adapter or skill is **Decision Kernel Compatible** if it:

✓ Passes Action Specification v1.0  
✓ Passes WorldState Specification v1.0  
✓ Passes Adapter Contract conformance  

Verify compatibility:
```bash
python -m decision_kernel_conformance your_adapter.YourAdapter
```

**Reference Implementations:**
- [decision-kernel-ros2](decision-kernel-ros2/) - ROS2 translation layer
- [decision-kernel-webots](decision-kernel-webots/) - Webots simulator adapter
- [MockRobot](adapters/mock/) - Built-in testing adapter

See [Compatibility Guide](docs/compatibility.md) for formal definition.  
See [registry/compatible_adapters.yaml](registry/compatible_adapters.yaml) for full list.

## Documentation

### Getting Started
- [60-Minute Tutorial](docs/teaching/60_minute_tutorial.md) - Learn Decision Kernel (v0.8+)
- [Adoption Guide](docs/adoption.md) - Integrate into your robot (v0.6+)
- [Adopters Guide](docs/adopters.md) - Who should use Decision Kernel (v0.8+)

### Technical
- [Whitepaper](docs/papers/decision_kernel_whitepaper.md) - Academic technical paper (v0.8+)
- [Architecture](docs/architecture.md) - System design and module boundaries
- [Compatibility Guide](docs/compatibility.md) - Formal compatibility definition (v0.7+)
- [Reference Implementations](docs/reference_implementations.md) - Reference adapters and skills (v0.7+)

### Specifications
- [Action Specification](docs/action_spec.md) - Action schema and validation (v0.3+)
- [WorldState Specification](docs/world_state_spec.md) - World state schema (v0.3+)
- [Adapter Contract](docs/adapter_contract.md) - Adapter interface requirements (v0.3+)
- [Skill Specification](docs/skill_spec.md) - Reusable behavior templates (v0.2+)
- [Conformance Testing](docs/conformance.md) - Verify adapter compatibility (v0.4+)

### Project
- [Vision](docs/vision.md) - Why robot brains need a kernel (v0.5+)
- [Roadmap](docs/roadmap.md) - v1.0 criteria and direction (v0.8+)
- [Governance](GOVERNANCE.md) - Project governance (v0.5+)
- [Contributing](CONTRIBUTING.md) - Development guidelines
- [Changelog](CHANGELOG.md) - Version history
- [Security](SECURITY.md) - Vulnerability reporting

## Ecosystem

- [Ecosystem Kit](decision-kernel-ecosystem-kit/) - Templates and publishing guide (v0.6+)
- [Compatible Adapters](registry/compatible_adapters.yaml) - Community adapters (v0.6+)
- [Compatible Skills](registry/compatible_skills.yaml) - Community skills (v0.6+)

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## License

Apache License 2.0
