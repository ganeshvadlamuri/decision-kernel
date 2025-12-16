"""Tests for dynamic replanner"""
from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.planner.htn_planner import HTNPlanner
from brain.planner.replanner import Replanner
from brain.world.extended_state import ExtendedWorldState


class TestReplanner:
    """Test dynamic replanning on failures"""

    def setup_method(self):
        self.base_planner = HTNPlanner()
        self.replanner = Replanner(self.base_planner)
        self.state = ExtendedWorldState(
            robot_location='home',
            human_location='living_room',
            battery_level=80.0
        )

    def test_blocked_path_recovery(self):
        """Test: Replans when path is blocked"""
        goal = Goal(action='bring', target='water')
        failed_action = Action('navigate_to', location='kitchen')
        remaining = [Action('grasp', target='water')]

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'path_blocked', self.state, remaining
        )

        assert len(new_plan) > 0
        assert 'find_alternative_route' in [a.action_type for a in new_plan]
        assert 'Recovered' in reason

    def test_object_not_found_recovery(self):
        """Test: Searches for missing object"""
        goal = Goal(action='bring', target='keys')
        failed_action = Action('grasp', target='keys')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'object_not_found', self.state, remaining
        )

        assert len(new_plan) > 0
        action_types = [a.action_type for a in new_plan]
        assert 'navigate_to' in action_types
        assert 'search_area' in action_types

    def test_heavy_object_recovery(self):
        """Test: Requests help for heavy object"""
        goal = Goal(action='grasp', target='table')
        failed_action = Action('grasp', target='table')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'object_too_heavy', self.state, remaining
        )

        assert len(new_plan) > 0
        action_types = [a.action_type for a in new_plan]
        assert 'alert_human' in action_types
        assert 'wait_for_human' in action_types

    def test_locked_door_recovery(self):
        """Test: Finds key for locked door"""
        goal = Goal(action='navigate_to', location='room_305')
        failed_action = Action('open_door', location='room_305')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'locked', self.state, remaining
        )

        assert len(new_plan) > 0
        action_types = [a.action_type for a in new_plan]
        assert 'search_for_key' in action_types
        assert 'unlock_door' in action_types

    def test_low_battery_recovery(self):
        """Test: Charges when battery low during navigation"""
        goal = Goal(action='navigate_to', location='kitchen')
        failed_action = Action('navigate_to', location='kitchen')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'low_battery', self.state, remaining
        )

        assert len(new_plan) > 0
        action_types = [a.action_type for a in new_plan]
        assert 'charge' in action_types
        assert 'navigate_to' in action_types

    def test_generic_navigation_failure(self):
        """Test: Generic navigation failure handler"""
        goal = Goal(action='navigate_to', location='kitchen')
        failed_action = Action('navigate_to', location='kitchen')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'unknown_error', self.state, remaining
        )

        assert len(new_plan) > 0
        action_types = [a.action_type for a in new_plan]
        assert 'stop' in action_types
        assert 'wait' in action_types

    def test_preserves_remaining_plan(self):
        """Test: Appends remaining plan after recovery"""
        goal = Goal(action='bring', target='water')
        failed_action = Action('navigate_to', location='kitchen')
        remaining = [
            Action('grasp', target='water'),
            Action('release', target='water')
        ]

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'path_blocked', self.state, remaining
        )

        # Should include recovery + remaining
        assert len(new_plan) >= len(remaining)
        # Last actions should be from remaining plan
        assert new_plan[-1].action_type == 'release'

    def test_full_replan_fallback(self):
        """Test: Falls back to full replan when no handler"""
        goal = Goal(action='make_coffee', target='coffee')
        failed_action = Action('brew_coffee')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'machine_broken', self.state, remaining
        )

        # Should generate new full plan
        assert len(new_plan) > 0
        assert 'replan' in reason.lower()

    def test_no_recovery_returns_empty(self):
        """Test: Returns empty when no recovery possible"""
        goal = Goal(action='impossible_task')
        failed_action = Action('impossible_action')
        remaining = []

        new_plan, reason = self.replanner.replan(
            goal, failed_action, 'impossible', self.state, remaining
        )

        assert len(new_plan) == 0
        assert 'No recovery' in reason
