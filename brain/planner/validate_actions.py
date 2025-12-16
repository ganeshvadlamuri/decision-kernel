"""Action validation utilities"""

import re

from brain.planner.actions import Action


def validate_action(action: Action) -> tuple[bool, str]:
    """Validate action conforms to v1.0 spec"""

    if not isinstance(action.action_type, str):
        return False, "action_type must be string"

    if not action.action_type:
        return False, "action_type must be non-empty"

    if not re.match(r"^\d+\.\d+$", action.version):
        return False, f"version must match pattern 'X.Y', got: {action.version}"

    if action.target is not None and not isinstance(action.target, str):
        return False, "target must be string or None"

    if action.location is not None and not isinstance(action.location, str):
        return False, "location must be string or None"

    if not isinstance(action.parameters, dict):
        return False, "parameters must be dict"

    return True, "valid"


def validate_action_list(actions: list[Action]) -> tuple[bool, str]:
    """Validate list of actions"""

    if not isinstance(actions, list):
        return False, "actions must be a list"

    for i, action in enumerate(actions):
        if not isinstance(action, Action):
            return False, f"action {i} is not an Action instance"

        is_valid, reason = validate_action(action)
        if not is_valid:
            return False, f"action {i}: {reason}"

    return True, "valid"
