# Skill Specification

## Overview

Skills are reusable behavior templates that extend the planner's capabilities without modifying core kernel logic. They define structured action sequences with parameter substitution.

## What is a Skill?

A skill encapsulates:
- A named behavior (e.g., "bring", "pick_and_place")
- Required inputs and their types
- Preconditions that must be true
- Expected effects after execution
- An action sequence template

## Required Fields

```python
@dataclass
class Skill:
    name: str                           # Unique identifier
    description: str                    # Human-readable description
    inputs: dict[str, str]              # Input parameters and types
    preconditions: list[str]            # Required conditions
    effects: list[str]                  # Expected outcomes
    action_sequence: list[dict[str, str]]  # Action templates
```

## Action Sequence Format

Each action in the sequence is a dictionary with:
- `type`: Action type (e.g., "navigate_to", "grasp")
- `target`: Optional target object (supports `{target}` substitution)
- `location`: Optional location (supports `{target_location}`, `{human_location}`)

## Parameter Substitution

The planner substitutes placeholders at planning time:
- `{target}` → goal.target
- `{target_location}` → location of target object in world state
- `{human_location}` → world_state.human_location

## How the Planner Uses Skills

1. Parse human intent into Goal
2. Check if Goal.action matches a registered skill name
3. If match found, use skill's action_sequence with parameter substitution
4. If no match, fallback to naive planning

## Example: Bring Skill

```python
from brain.skills.skill import Skill

bring_skill = Skill(
    name="bring",
    description="Bring an object to the human",
    inputs={"target": "object to bring"},
    preconditions=["object exists", "object is graspable"],
    effects=["object at human location"],
    action_sequence=[
        {"type": "navigate_to", "location": "{target_location}"},
        {"type": "grasp", "target": "{target}"},
        {"type": "navigate_to", "location": "{human_location}"},
        {"type": "release", "target": "{target}"},
    ],
)
```

## Registering Skills

Skills must be explicitly registered:

```python
from brain.skills.registry import SkillRegistry
from brain.kernel import RobotBrainKernel

registry = SkillRegistry()
registry.register(bring_skill)

kernel = RobotBrainKernel(skill_registry=registry)
```

## Design Principles

- **Optional**: Skills are opt-in, existing behavior unchanged
- **Explicit**: No magic globals, explicit registration required
- **Minimal**: Simple data structures, no complex logic
- **Extensible**: Easy to add new skills without kernel changes

## Limitations

- No conditional logic in action sequences
- No loops or branching
- Parameter substitution is simple string replacement
- Preconditions are declarative only (not enforced)

For complex behaviors, implement custom planner logic or use adapters.
