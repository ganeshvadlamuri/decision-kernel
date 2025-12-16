"""Tests for Action specification conformance"""

from brain.planner.actions import Action
from brain.planner.validate_actions import validate_action, validate_action_list


def test_action_has_required_fields():
    """Action must have required fields"""
    action = Action("test_action")
    assert hasattr(action, "action_type")
    assert hasattr(action, "target")
    assert hasattr(action, "location")
    assert hasattr(action, "parameters")
    assert hasattr(action, "version")


def test_action_version_field():
    """Action must have version field with default"""
    action = Action("test")
    assert action.version == "1.0"


def test_action_parameters_field():
    """Action must have parameters field with default"""
    action = Action("test")
    assert action.parameters == {}


def test_action_backward_compatible():
    """v0.1-v0.2 Action construction still works"""
    action = Action("navigate_to", location="kitchen")
    assert action.action_type == "navigate_to"
    assert action.location == "kitchen"
    assert action.target is None


def test_validate_action_valid():
    """Valid actions pass validation"""
    action = Action("grasp", target="cup")
    is_valid, msg = validate_action(action)
    assert is_valid
    assert msg == "valid"


def test_validate_action_empty_type():
    """Empty action_type fails validation"""
    action = Action("")
    is_valid, msg = validate_action(action)
    assert not is_valid
    assert "non-empty" in msg


def test_validate_action_invalid_version():
    """Invalid version format fails validation"""
    action = Action("test")
    action.version = "invalid"
    is_valid, msg = validate_action(action)
    assert not is_valid
    assert "version" in msg


def test_validate_action_list_valid():
    """Valid action list passes validation"""
    actions = [
        Action("navigate_to", location="kitchen"),
        Action("grasp", target="cup"),
    ]
    is_valid, msg = validate_action_list(actions)
    assert is_valid


def test_validate_action_list_invalid():
    """Invalid action in list fails validation"""
    actions = [Action("valid"), Action("")]
    is_valid, msg = validate_action_list(actions)
    assert not is_valid


def test_action_with_parameters():
    """Actions can include custom parameters"""
    action = Action("grasp", target="cup", parameters={"force": "gentle"})
    assert action.parameters["force"] == "gentle"
    is_valid, _ = validate_action(action)
    assert is_valid
