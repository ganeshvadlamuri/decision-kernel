# Reference Implementations

Official reference implementations maintained by the Decision Kernel project.

## Why Reference Implementations Matter

Reference implementations serve as:

1. **Proof of concept** - Demonstrate cross-environment viability
2. **Implementation guide** - Show correct adapter patterns
3. **Conformance baseline** - Define expected behavior
4. **Testing standard** - Validate kernel changes
5. **Community template** - Provide starting point for new adapters

Reference implementations are **not production systems**. They are **educational and validation tools**.

## Reference Adapters

### ROS2 Adapter

**Repository**: [decision-kernel-ros2](../decision-kernel-ros2/)  
**Status**: Reference implementation  
**Environment**: ROS2 middleware

**Purpose**:
- Prove Decision Kernel works with ROS2
- Demonstrate translation layer pattern
- Show middleware integration

**Scope**:
- Translates ROS2 topics to WorldState
- Translates Actions to ROS2 messages
- Does NOT control hardware
- Does NOT implement autonomy

**Conformance**: ✓ 4/4 tests passed

**Usage**:
```python
from decision_kernel_ros2.adapter import ROS2Adapter
from brain.kernel import RobotBrainKernel

adapter = ROS2Adapter()
kernel = RobotBrainKernel(adapter=adapter)
```

**Key Insight**: ROS2 is a communication layer, not a decision layer. Decision Kernel provides the missing orchestration.

---

### Webots Adapter

**Repository**: [decision-kernel-webots](../decision-kernel-webots/)  
**Status**: Reference implementation  
**Environment**: Webots simulator

**Purpose**:
- Prove Decision Kernel works in simulation
- Demonstrate non-ROS integration
- Show simulator adapter pattern

**Scope**:
- Translates Webots world data to WorldState
- Translates Actions to Webots commands
- Does NOT implement physics
- Does NOT implement perception

**Conformance**: ✓ 4/4 tests passed

**Usage**:
```python
from decision_kernel_webots.adapter import WebotsAdapter
from brain.kernel import RobotBrainKernel

adapter = WebotsAdapter()
kernel = RobotBrainKernel(adapter=adapter)
```

**Key Insight**: Simulators provide environment, not decision-making. Decision Kernel provides consistent planning across sim and real.

---

### Mock Adapter

**Repository**: [adapters/mock](../adapters/mock/)  
**Status**: Built-in reference  
**Environment**: Testing

**Purpose**:
- Enable testing without hardware
- Demonstrate minimal adapter
- Validate kernel behavior

**Scope**:
- Returns fixed WorldState
- Logs actions without execution
- Minimal implementation

**Conformance**: ✓ 4/4 tests passed

**Usage**:
```python
from adapters.mock.mock_robot import MockRobot
from brain.kernel import RobotBrainKernel

adapter = MockRobot()
kernel = RobotBrainKernel(adapter=adapter)
```

**Key Insight**: Adapters can be trivial. The kernel handles complexity.

---

## Reference Skills

### Bring Water Skill

**Repository**: [brain/skills/builtin.py](../brain/skills/builtin.py)  
**Status**: Built-in reference  
**Intent**: "bring {target}"

**Purpose**:
- Demonstrate skill structure
- Show action sequence composition
- Provide reusable behavior template

**Definition**:
```python
Skill(
    name="bring",
    intent_pattern="bring {target}",
    action_sequence=[
        {"type": "navigate_to", "location": "{target_location}"},
        {"type": "grasp", "target": "{target}"},
        {"type": "navigate_to", "location": "{human_location}"},
        {"type": "release", "target": "{target}"},
    ],
)
```

**Key Insight**: Skills are data, not code. They compose actions, not implement them.

---

## What Makes a Reference Implementation

### Requirements

1. **Passes conformance** - 4/4 tests
2. **Documented scope** - Clear what it does/doesn't do
3. **Minimal complexity** - Only essential code
4. **Educational value** - Teaches correct patterns
5. **Maintained** - Updated with kernel changes

### Non-Requirements

- Production readiness
- Performance optimization
- Feature completeness
- Hardware support
- Safety certification

Reference implementations prioritize **clarity over capability**.

## Using Reference Implementations

### As Learning Tools

Study reference implementations to understand:
- Adapter contract requirements
- Data translation patterns
- Scope boundaries
- Testing approaches

### As Starting Points

Fork reference implementations to create:
- Custom adapters for your hardware
- Environment-specific integrations
- Production-ready systems

### As Validation Tools

Use reference implementations to:
- Test kernel changes
- Verify conformance
- Validate specifications
- Benchmark behavior

## Reference vs Production

| Aspect | Reference | Production |
|--------|-----------|------------|
| Purpose | Education | Deployment |
| Complexity | Minimal | Full |
| Testing | Conformance | Comprehensive |
| Performance | Adequate | Optimized |
| Safety | Not certified | Certified |
| Maintenance | Kernel team | Adapter owner |

Reference implementations are **starting points**, not **end points**.

## Multi-Environment Proof

Decision Kernel reference implementations span:

- **ROS2** - Industry standard middleware
- **Webots** - Academic simulator
- **Mock** - Pure software testing

This proves Decision Kernel is:
- Environment-agnostic
- Middleware-neutral
- Hardware-independent
- Universally applicable

## Contributing Reference Implementations

To propose a new reference implementation:

1. Implement adapter following contract
2. Pass conformance tests
3. Document scope and non-goals
4. Provide minimal demo
5. Submit proposal via GitHub issue

Criteria for acceptance:
- Demonstrates new environment class
- Educational value to community
- Maintainable by core team
- Minimal dependencies

## Maintenance Policy

Reference implementations:
- Updated for breaking kernel changes
- Kept minimal and focused
- Documented thoroughly
- Tested in CI

Community adapters:
- Maintained by authors
- Listed in registry
- Not guaranteed updated

## Summary

Reference implementations:
- ✓ Prove cross-environment viability
- ✓ Demonstrate correct patterns
- ✓ Provide educational value
- ✓ Validate kernel behavior
- ✗ Are NOT production systems
- ✗ Are NOT feature-complete
- ✗ Are NOT performance-optimized

Use them to learn, validate, and start. Build on them for production.

---

**Current Reference Implementations:**
- ROS2 Adapter (middleware)
- Webots Adapter (simulation)
- Mock Adapter (testing)
- Bring Water Skill (behavior)

**Statement**: Decision Kernel runs on ROS2, Webots, and mock environments.

**Implication**: Decision Kernel is environment-agnostic infrastructure.
