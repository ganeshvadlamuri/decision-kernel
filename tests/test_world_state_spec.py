"""Tests for WorldState specification conformance"""

import time

from brain.world.objects import WorldObject
from brain.world.state import WorldState
from brain.world.validate import validate_world_state


def test_world_state_has_required_fields():
    """WorldState must have all required fields"""
    state = WorldState()
    assert hasattr(state, "objects")
    assert hasattr(state, "robot_location")
    assert hasattr(state, "human_location")
    assert hasattr(state, "locations")
    assert hasattr(state, "timestamp")
    assert hasattr(state, "frame_id")
    assert hasattr(state, "relations")


def test_world_state_timestamp_default():
    """WorldState timestamp defaults to current time"""
    before = time.time()
    state = WorldState()
    after = time.time()
    assert before <= state.timestamp <= after


def test_world_state_frame_id_default():
    """WorldState frame_id defaults to 'world'"""
    state = WorldState()
    assert state.frame_id == "world"


def test_world_state_relations_default():
    """WorldState relations defaults to empty dict"""
    state = WorldState()
    assert state.relations == {}


def test_world_state_backward_compatible():
    """v0.1-v0.2 WorldState construction still works"""
    state = WorldState(
        objects=[WorldObject("cup", "kitchen", "container")],
        robot_location="home",
        human_location="home",
        locations=["home"],
    )
    assert state.robot_location == "home"
    assert len(state.objects) == 1


def test_validate_world_state_valid():
    """Valid WorldState passes validation"""
    state = WorldState(
        objects=[],
        robot_location="home",
        human_location="home",
        locations=["home"],
        timestamp=time.time(),
    )
    is_valid, msg = validate_world_state(state)
    assert is_valid
    assert msg == "valid"


def test_validate_world_state_empty_robot_location():
    """Empty robot_location fails validation"""
    state = WorldState(robot_location="", human_location="home", timestamp=time.time())
    is_valid, msg = validate_world_state(state)
    assert not is_valid
    assert "robot_location" in msg


def test_validate_world_state_invalid_timestamp():
    """Invalid timestamp fails validation"""
    state = WorldState(
        robot_location="home", human_location="home", timestamp=-1.0
    )
    is_valid, msg = validate_world_state(state)
    assert not is_valid
    assert "timestamp" in msg


def test_validate_world_state_empty_frame_id():
    """Empty frame_id fails validation"""
    state = WorldState(
        robot_location="home",
        human_location="home",
        timestamp=time.time(),
        frame_id="",
    )
    is_valid, msg = validate_world_state(state)
    assert not is_valid
    assert "frame_id" in msg


def test_world_state_with_relations():
    """WorldState can include relations"""
    state = WorldState(
        objects=[WorldObject("cup", "table", "container")],
        robot_location="kitchen",
        human_location="living_room",
        locations=["kitchen", "living_room"],
        timestamp=time.time(),
        relations={"cup": {"on": "table"}},
    )
    is_valid, _ = validate_world_state(state)
    assert is_valid
    assert state.relations["cup"]["on"] == "table"
