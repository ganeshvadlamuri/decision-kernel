"""WorldState validation utilities"""

from brain.world.objects import WorldObject
from brain.world.state import WorldState


def validate_world_state(state: WorldState) -> tuple[bool, str]:
    """Validate WorldState conforms to v1.0 spec"""

    if not isinstance(state.objects, list):
        return False, "objects must be a list"

    for i, obj in enumerate(state.objects):
        if not isinstance(obj, WorldObject):
            return False, f"objects[{i}] is not a WorldObject"

    if not isinstance(state.robot_location, str):
        return False, "robot_location must be string"

    if not state.robot_location:
        return False, "robot_location must be non-empty"

    if not isinstance(state.human_location, str):
        return False, "human_location must be string"

    if not state.human_location:
        return False, "human_location must be non-empty"

    if not isinstance(state.locations, list):
        return False, "locations must be a list"

    for i, loc in enumerate(state.locations):
        if not isinstance(loc, str):
            return False, f"locations[{i}] must be string"

    if not isinstance(state.timestamp, (int, float)):
        return False, "timestamp must be numeric"

    if state.timestamp <= 0:
        return False, "timestamp must be positive"

    if not isinstance(state.frame_id, str):
        return False, "frame_id must be string"

    if not state.frame_id:
        return False, "frame_id must be non-empty"

    if not isinstance(state.relations, dict):
        return False, "relations must be dict"

    return True, "valid"
