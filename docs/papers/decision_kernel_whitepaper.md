# Decision Kernel: A Hardware-Agnostic Decision Interface for Robots

**Version**: 0.8.0  
**Date**: February 2024  
**Status**: Technical Whitepaper

## Abstract

We present Decision Kernel, a minimal orchestration layer that separates decision logic from hardware execution in robotic systems. Decision Kernel provides a stable interface between human intent and robot actions, enabling hardware-agnostic planning while delegating perception, motion planning, and control to existing subsystems. We demonstrate cross-environment viability through reference implementations on ROS2 middleware and Webots simulator, and define formal compatibility contracts for ecosystem integration.

## 1. Problem Definition

### 1.1 The Decision-Execution Gap

Modern robotic systems conflate three distinct concerns:

1. **Decision-making**: What actions achieve a goal?
2. **Motion planning**: How to execute actions physically?
3. **Hardware control**: How to command actuators?

This conflation creates:
- Hardware lock-in (decisions tied to specific platforms)
- Middleware dependency (autonomy requires specific communication layers)
- Reusability barriers (behaviors cannot transfer across systems)

### 1.2 Formal Problem Statement

**Given**:
- Human intent I (natural language or structured goal)
- World state W (environment representation)
- Action space A (available robot capabilities)

**Find**:
- Action sequence π = [a₁, a₂, ..., aₙ] where aᵢ ∈ A
- Such that executing π achieves I
- Subject to safety constraints S

**Without**:
- Assuming specific hardware platform
- Requiring specific middleware
- Implementing motion planning or control

### 1.3 Non-Problem

Decision Kernel does NOT solve:
- Motion planning (path generation)
- Perception (object detection, localization)
- Control (trajectory execution, PID loops)
- Learning (policy optimization, adaptation)

These remain responsibilities of existing subsystems.

## 2. System Model

### 2.1 Architecture

```
Human Intent → Decision Kernel → Hardware Adapter → Robot
                    ↓
              [Planning]
              [Safety]
              [Memory]
```

**Components**:
- **Intent Parser**: I → Goal
- **Planner**: (Goal, W) → π
- **Safety Validator**: π → {valid, invalid}
- **Memory**: Store execution history
- **Adapter**: Translate between kernel and hardware

### 2.2 Data Model

**WorldState** W:
```
W = {
  objects: [Object],
  robot_location: Location,
  human_location: Location,
  locations: [Location],
  timestamp: Time,
  frame_id: String,
  relations: Map<Object, Relation>
}
```

**Action** a:
```
a = {
  action_type: String,
  target: Optional<Object>,
  location: Optional<Location>,
  parameters: Map<String, Value>,
  version: String
}
```

**Plan** π:
```
π = [a₁, a₂, ..., aₙ]
```

### 2.3 Adapter Contract

Adapters implement three methods:

```
sense() → WorldState
execute(Plan) → ExecutionReport
capabilities() → {supported_actions, hardware, version}
```

**Invariants**:
1. sense() returns valid WorldState
2. execute() only receives actions in supported_actions
3. capabilities() declares all supported operations

### 2.4 Guarantees

Decision Kernel guarantees:
- **Safety validation**: All plans checked before execution
- **Capability checking**: Actions validated against adapter
- **Execution logging**: All decisions recorded
- **Interface stability**: Adapter contract remains stable

Decision Kernel does NOT guarantee:
- Plan optimality
- Execution success
- Real-time performance
- Hardware safety

## 3. Comparison with Existing Approaches

### 3.1 ROS (Robot Operating System)

**ROS provides**: Communication middleware, hardware drivers, tools

**ROS does not provide**: Decision orchestration, intent parsing, safety validation

**Relationship**: Decision Kernel uses ROS via adapters. ROS handles communication; Decision Kernel handles decisions.

**Key difference**: ROS is infrastructure for robot software. Decision Kernel is infrastructure for robot decisions.

### 3.2 Behavior Trees

**Behavior Trees provide**: Reactive control flow, modularity, visual design

**Behavior Trees do not provide**: Intent parsing, world state management, hardware abstraction

**Relationship**: Complementary. Behavior Trees can implement planner or adapter logic.

**Key difference**: Behavior Trees specify how to execute. Decision Kernel specifies what to execute.

### 3.3 Classical Task Planning

**Task Planners provide**: Optimal action sequences, formal guarantees, search algorithms

**Task Planners do not provide**: Hardware integration, real-time execution, world state sensing

**Relationship**: Task planners can replace Decision Kernel's naive planner.

**Key difference**: Task planners focus on optimality. Decision Kernel focuses on integration.

### 3.4 Closed Commercial Systems

**Commercial Systems provide**: End-to-end solutions, vendor support, integrated hardware

**Commercial Systems do not provide**: Hardware portability, vendor neutrality, open interfaces

**Relationship**: Incompatible. Commercial systems are vertically integrated.

**Key difference**: Commercial systems optimize for specific use cases. Decision Kernel optimizes for portability.

## 4. Implementation

### 4.1 Core Kernel

**Language**: Python 3.10+  
**Dependencies**: PyYAML (configuration only)  
**Size**: ~1000 lines of code (brain/ directory)

**Modules**:
- `brain/intent/` - Intent parsing
- `brain/planner/` - Action sequence generation
- `brain/safety/` - Constraint validation
- `brain/memory/` - Execution logging
- `brain/world/` - State representation

### 4.2 Reference Adapters

**ROS2 Adapter**:
- Translates ROS2 topics to WorldState
- Publishes actions to ROS2 topics
- Does not control hardware directly

**Webots Adapter**:
- Reads Webots world data
- Logs intended Webots commands
- Does not execute physics simulation

**Mock Adapter**:
- Returns fixed WorldState
- Logs actions without execution
- Enables testing without hardware

### 4.3 Conformance Testing

Adapters verified via automated conformance tests:

```
Test 1: Method presence (sense, execute, capabilities)
Test 2: sense() returns valid WorldState
Test 3: execute() returns valid ExecutionReport
Test 4: capabilities() returns required keys
```

Pass rate: 4/4 required for compatibility.

## 5. Evaluation

### 5.1 Cross-Environment Viability

Decision Kernel demonstrated on:
- **ROS2**: Industry middleware standard
- **Webots**: Academic simulator
- **Mock**: Pure software testing

**Result**: Same kernel code runs unchanged across all environments.

### 5.2 Adapter Complexity

Reference adapter implementations:
- ROS2: ~150 lines
- Webots: ~140 lines
- Mock: ~80 lines

**Result**: Minimal adapter complexity validates thin interface design.

### 5.3 Conformance Validation

All reference adapters pass conformance:
- ROS2: 4/4 tests
- Webots: 4/4 tests
- Mock: 4/4 tests

**Result**: Formal contract enables automated verification.

### 5.4 Backward Compatibility

Versions 0.1 through 0.8:
- Zero breaking changes
- All tests passing (57/57)
- Stable adapter contract

**Result**: Interface stability maintained across 8 releases.

## 6. Reproducible Demonstrations

### 6.1 ROS2 Demo

**Setup**: No ROS2 installation required (simulated topics)

**Command**:
```bash
python -m demos.ros2_hello_world.run
```

**Output**: Intent → WorldState → Plan → Execution (4 actions)

**Runtime**: <5 seconds

### 6.2 Webots Demo

**Setup**: No Webots installation required (mocked API)

**Command**:
```bash
cd decision-kernel-webots
python demo.py
```

**Output**: Intent → WorldState → Plan → Execution (4 actions)

**Runtime**: <5 seconds

### 6.3 Conformance Verification

**Command**:
```bash
python -m decision_kernel_conformance <adapter_module>.<AdapterClass>
```

**Output**: 4/4 tests passed or failure details

**Runtime**: <1 second

## 7. Formal Specifications

### 7.1 Action Specification v1.0

Defines Action dataclass structure, required fields, validation rules.

**Reference**: docs/action_spec.md

### 7.2 WorldState Specification v1.0

Defines WorldState dataclass structure, required fields, validation rules.

**Reference**: docs/world_state_spec.md

### 7.3 Adapter Contract v1.0

Defines adapter interface, method signatures, return types, invariants.

**Reference**: docs/adapter_contract.md

### 7.4 Compatibility Definition

Defines "Decision Kernel Compatible" status, verification process, version rules.

**Reference**: docs/compatibility.md

## 8. Limitations

### 8.1 Planning

Current planner is naive symbolic planner. Does not:
- Optimize for cost or time
- Handle partial observability
- Perform search or backtracking
- Learn from experience

**Mitigation**: Planner is replaceable. Advanced planners can integrate via same interface.

### 8.2 Safety

Current safety validator checks basic constraints. Does not:
- Verify physical feasibility
- Predict collision
- Guarantee hardware safety
- Certify for production

**Mitigation**: Safety is adapter responsibility. Hardware-specific safety remains in adapters.

### 8.3 Performance

Not optimized for:
- Real-time execution
- High-frequency control
- Large state spaces
- Distributed systems

**Mitigation**: Decision Kernel targets high-level decisions, not low-level control.

## 9. Related Work

**ROS/ROS2** [Quigley et al., 2009]: Middleware for robot software communication.

**Behavior Trees** [Colledanchise & Ögren, 2018]: Reactive control architecture for robotics.

**PDDL** [McDermott et al., 1998]: Planning Domain Definition Language for classical planning.

**SMACH** [Bohren & Cousins, 2010]: State machine library for ROS.

**FlexBE** [Schillinger et al., 2016]: Behavior engine for hierarchical state machines.

**py_trees** [Duckworth, 2019]: Python behavior tree implementation.

## 10. Future Work

### 10.1 Advanced Planning

Integration with:
- PDDL planners (Fast Downward, FF)
- Probabilistic planners (POMDP solvers)
- Learning-based planners (RL policies)

### 10.2 Formal Verification

- Temporal logic specifications
- Model checking integration
- Safety property verification

### 10.3 Multi-Robot Coordination

- Distributed decision-making
- Conflict resolution
- Resource allocation

### 10.4 Standardization

- IEEE/ISO specification process
- Industry working group
- Academic consortium

## 11. Conclusion

Decision Kernel provides a minimal, stable interface for robot decision-making that is independent of hardware, middleware, and execution environment. Through formal specifications, conformance testing, and reference implementations, we demonstrate that decision logic can be separated from execution infrastructure while maintaining practical utility.

The system's stability across 8 releases and viability across multiple environments (ROS2, Webots, Mock) suggests that hardware-agnostic decision interfaces are both feasible and valuable for the robotics community.

## Availability

**Source Code**: https://github.com/decision-kernel/decision-kernel  
**License**: Apache 2.0  
**Documentation**: https://github.com/decision-kernel/decision-kernel/tree/main/docs

## Acknowledgments

Decision Kernel is community-driven, vendor-neutral infrastructure. See GOVERNANCE.md for project governance and MAINTAINERS.md for contributor list.

## References

Bohren, J., & Cousins, S. (2010). The SMACH High-Level Executive. IEEE Robotics & Automation Magazine.

Colledanchise, M., & Ögren, P. (2018). Behavior Trees in Robotics and AI. CRC Press.

Duckworth, D. (2019). py_trees: Pythonic Behaviour Trees. https://github.com/splintered-reality/py_trees

McDermott, D., et al. (1998). PDDL - The Planning Domain Definition Language. Technical Report.

Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. ICRA Workshop on Open Source Software.

Schillinger, P., et al. (2016). Human-Robot Collaborative High-Level Control with Application to Rescue Robotics. IEEE International Conference on Robotics and Automation.
