"""Tests for capability gating"""

import pytest

from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


class LimitedAdapter:
    """Adapter with limited capabilities"""

    def capabilities(self):
        return {
            "supported_actions": ["navigate_to"],
            "hardware": "limited",
            "version": "1.0",
        }


class FullAdapter:
    """Adapter with full capabilities"""

    def capabilities(self):
        return {
            "supported_actions": ["navigate_to", "grasp", "release", "clean_area"],
            "hardware": "full",
            "version": "1.0",
        }


def test_capability_gating_blocks_unsupported_action():
    """Kernel rejects plan with unsupported actions"""
    adapter = LimitedAdapter()
    kernel = RobotBrainKernel(adapter=adapter)

    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living_room",
        human_location="living_room",
    )

    # "bring me water" requires grasp/release which LimitedAdapter doesn't support
    with pytest.raises(ValueError, match="does not support action"):
        kernel.process("bring me water", world)


def test_capability_gating_allows_supported_action():
    """Kernel accepts plan with only supported actions"""
    adapter = LimitedAdapter()
    kernel = RobotBrainKernel(adapter=adapter)

    world = WorldState()

    # "go to kitchen" only requires navigate_to which is supported
    plan = kernel.process("go to kitchen", world)
    assert len(plan) > 0


def test_capability_gating_with_full_adapter():
    """Full adapter supports all actions"""
    adapter = FullAdapter()
    kernel = RobotBrainKernel(adapter=adapter)

    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living_room",
        human_location="living_room",
    )

    # Should work with full adapter
    plan = kernel.process("bring me water", world)
    assert len(plan) == 4


def test_no_capability_check_without_adapter():
    """Kernel works without adapter (no capability checking)"""
    kernel = RobotBrainKernel(adapter=None)

    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living_room",
        human_location="living_room",
    )

    # Should work without adapter
    plan = kernel.process("bring me water", world)
    assert len(plan) == 4
