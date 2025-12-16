# Decision Kernel Architecture

## Overview

Decision Kernel is a minimal orchestration layer for robot decision-making. It processes human intent, generates action plans, validates safety, and maintains execution history.

## Core Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────┐    ┌────────┐
│ Intent  │───▶│ Planner │───▶│ Safety  │───▶│ Memory │───▶│ Action │
│ Parser  │    │         │    │ Checker │    │        │    │  Plan  │
└─────────┘    └─────────┘    └─────────┘    └────────┘    └────────┘
     │              │               │              │
     ▼              ▼               ▼              ▼
   Goal         Actions         Validated      Logged
  Schema        List            Plan           History
```

## Module Boundaries

### brain/ (Core Kernel)

Hardware-agnostic decision logic. No assumptions about:
- Physical hardware
- Sensor types
- Actuator types
- Communication protocols
- AI/ML frameworks
- ROS or middleware

**Modules:**

- **intent/** - Parse human commands into structured Goal objects
- **world/** - Maintain WorldState representation (objects, locations)
- **planner/** - Generate action sequences from goals
- **safety/** - Validate plans against constraints
- **memory/** - Store execution history
- **kernel.py** - Orchestrate the pipeline

### adapters/

Bridge kernel to real systems. Contains all hardware/framework integrations.

- **mock/** - Print actions (for testing)
- **ros/** - ROS integration (stub)
- **simulation/** - Sim environment (stub)

**Rule:** Adapters depend on brain/, never the reverse.

## Data Flow

1. **Input:** Human command (string) + WorldState
2. **Intent:** Parse to Goal(action, target, location, recipient)
3. **Planning:** Generate List[Action] to achieve goal
4. **Safety:** Validate plan against rules
5. **Memory:** Log goal + plan + outcome
6. **Output:** Return validated action plan

## What the Kernel Does

- Parse natural language intent
- Generate symbolic action plans
- Validate safety constraints
- Maintain execution history
- Provide clean adapter interface

## What the Kernel Does NOT Do

- Motion planning (trajectories, kinematics)
- Perception (vision, SLAM, object detection)
- Hardware control (motors, sensors, actuators)
- ROS communication (topics, services, actions)
- Cloud services (APIs, databases, ML inference)
- Hardcoded AI models (LLMs, neural networks)

## Extension Points

To add new capabilities:

1. **New action types:** Extend planner/actions.py
2. **New safety rules:** Add to safety/rules.py
3. **New hardware:** Create adapter in adapters/
4. **New intent patterns:** Extend intent/parser.py

## Design Principles

- **Minimal:** Only essential orchestration logic
- **Boring:** Predictable, testable, debuggable
- **Agnostic:** No hardware or framework assumptions
- **Extensible:** Clear boundaries for customization
- **Infrastructure:** Not a product, a foundation
