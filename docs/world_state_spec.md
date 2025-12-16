# World State Specification v1.0

## Overview

WorldState represents the robot's understanding of its environment. This specification defines required fields and validation rules.

## Schema

```python
@dataclass
class WorldState:
    objects: list[WorldObject]           # Required: objects in environment
    robot_location: str                  # Required: robot's current location
    human_location: str                  # Required: human's location
    locations: list[str]                 # Required: known locations
    timestamp: float                     # Required: state timestamp (Unix time)
    frame_id: str = "world"             # Required: coordinate frame
    relations: dict = field(default_factory=dict)  # Optional: object relations
```

## Required Fields

### objects (list[WorldObject])
- List of all known objects in environment
- May be empty list
- Each object must be valid WorldObject

### robot_location (str)
- Current location of robot
- Must be non-empty string
- Should match a location in `locations` list

### human_location (str)
- Current location of human/operator
- Must be non-empty string
- Should match a location in `locations` list

### locations (list[str])
- All known locations in environment
- May be empty list
- Each location must be non-empty string

### timestamp (float)
- Unix timestamp when state was captured
- Must be positive number
- Used for state freshness validation

### frame_id (str)
- Coordinate frame reference
- Default: "world"
- Must be non-empty string

## Optional Fields

### relations (dict)
- Spatial or semantic relationships between objects
- Examples: {"cup": {"on": "table"}, "book": {"near": "lamp"}}
- Flexible structure for domain-specific needs

## WorldObject Schema

```python
@dataclass
class WorldObject:
    name: str                    # Required: unique identifier
    location: str                # Required: object location
    object_type: str             # Required: object category
    graspable: bool = True       # Optional: can be grasped
    position: tuple | None = None  # Optional: 3D coordinates
```

## Validation Rules

1. All required fields must be present
2. objects must be list of WorldObject instances
3. robot_location and human_location must be non-empty strings
4. locations must be list of strings
5. timestamp must be positive float
6. frame_id must be non-empty string
7. relations must be dict

## Backward Compatibility

v1.0 maintains compatibility with v0.1-v0.2:
- timestamp defaults to current time if not provided
- frame_id defaults to "world"
- relations defaults to empty dict
- Existing WorldState construction still works

## Examples

### Minimal WorldState
```python
import time

WorldState(
    objects=[],
    robot_location="home",
    human_location="home",
    locations=["home"],
    timestamp=time.time(),
    frame_id="world"
)
```

### Complete WorldState
```python
WorldState(
    objects=[
        WorldObject("cup", "kitchen", "container"),
        WorldObject("water", "kitchen", "liquid"),
    ],
    robot_location="living_room",
    human_location="living_room",
    locations=["kitchen", "living_room", "bedroom"],
    timestamp=time.time(),
    frame_id="world",
    relations={"cup": {"on": "counter"}}
)
```

## Version History

- v1.0 (v0.3): Initial specification with timestamp and frame_id
