# Action Specification v1.0

## Overview

Actions are the fundamental execution primitives in decision-kernel. This specification defines the stable schema for Action objects.

## Schema

```python
@dataclass
class Action:
    action_type: str              # Required: action identifier
    target: str | None = None     # Optional: target object
    location: str | None = None   # Optional: target location
    parameters: dict = field(default_factory=dict)  # Optional: additional params
    version: str = "1.0"          # Schema version
```

## Required Fields

### action_type (str)
- Unique identifier for the action
- Must be non-empty string
- Examples: "navigate_to", "grasp", "release", "clean_area"
- Convention: lowercase with underscores

### version (str)
- Schema version for compatibility tracking
- Default: "1.0"
- Format: semantic versioning (major.minor)

## Optional Fields

### target (str | None)
- Object being manipulated
- Examples: "cup", "water", "book"
- None if action has no target

### location (str | None)
- Spatial location for action
- Examples: "kitchen", "living room", "table"
- None if action has no location

### parameters (dict)
- Additional action-specific parameters
- Flexible key-value pairs
- Examples: {"speed": "slow", "force": "gentle"}

## Validation Rules

1. action_type must be non-empty string
2. version must match pattern: "\d+\.\d+"
3. target and location must be strings or None
4. parameters must be a dictionary

## String Representation

Actions should provide human-readable string format:
```
action_type(target=X, location=Y)
```

## Backward Compatibility

v1.0 maintains compatibility with v0.1-v0.2:
- Existing Action(action_type, target, location) still works
- version field has default value
- parameters field has default empty dict

## Examples

### Navigate Action
```python
Action(
    action_type="navigate_to",
    location="kitchen",
    version="1.0"
)
```

### Grasp Action
```python
Action(
    action_type="grasp",
    target="cup",
    parameters={"force": "gentle"},
    version="1.0"
)
```

### Release Action
```python
Action(
    action_type="release",
    target="cup",
    location="table",
    version="1.0"
)
```

## Version History

- v1.0 (v0.3): Initial specification with version field and parameters
