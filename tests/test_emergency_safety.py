"""Tests for emergency safety validator"""
from brain.planner.actions import Action
from brain.safety.emergency_rules import EmergencySafetyValidator
from brain.world.extended_state import ExtendedWorldState


class TestEmergencySafety:
    """Test emergency detection and safety validation"""

    def setup_method(self):
        self.validator = EmergencySafetyValidator()
        self.state = ExtendedWorldState(
            robot_location='home',
            human_location='living_room',
            battery_level=80.0
        )

    def test_detect_fire_emergency(self):
        """Test: Detects fire emergency"""
        self.state.trigger_emergency('fire', 'kitchen')

        is_emergency, etype = self.validator.detect_emergency(self.state)
        assert is_emergency
        assert etype == 'fire'

    def test_detect_intrusion_emergency(self):
        """Test: Detects intrusion emergency"""
        self.state.trigger_emergency('intrusion', 'back_door')

        is_emergency, etype = self.validator.detect_emergency(self.state)
        assert is_emergency
        assert etype == 'intrusion'

    def test_detect_fall_emergency(self):
        """Test: Detects fall emergency"""
        self.state.trigger_emergency('fall')

        is_emergency, etype = self.validator.detect_emergency(self.state)
        assert is_emergency
        assert etype == 'fall'

    def test_detect_critical_battery(self):
        """Test: Detects critical battery"""
        self.state.battery_level = 3.0

        is_emergency, etype = self.validator.detect_emergency(self.state)
        assert is_emergency
        assert etype == 'low_battery_critical'

    def test_fire_protocol_plan(self):
        """Test: Fire protocol generates evacuation plan"""
        plan = self.validator.get_emergency_plan('fire', self.state)

        action_types = [a.action_type for a in plan]
        assert 'sound_alarm' in action_types
        assert 'alert_human' in action_types
        assert 'call_emergency' in action_types
        assert 'navigate_to_exit' in action_types

    def test_intrusion_protocol_plan(self):
        """Test: Intrusion protocol generates security plan"""
        self.state.trigger_emergency('intrusion', 'back_door')
        plan = self.validator.get_emergency_plan('intrusion', self.state)

        action_types = [a.action_type for a in plan]
        assert 'sound_alarm' in action_types
        assert 'alert_human' in action_types
        assert 'call_emergency' in action_types
        assert 'record_video' in action_types

    def test_fall_protocol_plan(self):
        """Test: Fall protocol generates medical response"""
        plan = self.validator.get_emergency_plan('fall', self.state)

        action_types = [a.action_type for a in plan]
        assert 'alert_human' in action_types
        assert 'call_emergency' in action_types
        assert 'monitor_vital_signs' in action_types

    def test_validate_rejects_plan_during_emergency(self):
        """Test: Rejects normal plan during emergency"""
        self.state.trigger_emergency('fire', 'kitchen')
        plan = [Action('navigate_to', location='kitchen')]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'EMERGENCY' in msg
        assert 'fire' in msg

    def test_validate_rejects_critical_battery_without_charging(self):
        """Test: Rejects plan when battery critical and no charging"""
        self.state.battery_level = 3.0
        plan = [Action('navigate_to', location='kitchen')]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'CRITICAL' in msg
        assert 'Battery' in msg

    def test_validate_accepts_plan_with_charging(self):
        """Test: Accepts plan that includes charging"""
        self.state.battery_level = 10.0  # Above critical threshold
        plan = [
            Action('navigate_to', location='charging_station'),
            Action('charge')
        ]

        valid, msg = self.validator.validate(plan, self.state)
        assert valid

    def test_validate_rejects_insufficient_battery(self):
        """Test: Rejects plan requiring more battery than available"""
        self.state.battery_level = 10.0
        # 20 actions * 2% = 40% needed, but only 10% available
        plan = [Action('navigate_to', location='kitchen') for _ in range(20)]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'Insufficient battery' in msg

    def test_validate_rejects_blocked_path_without_alternative(self):
        """Test: Rejects navigation to blocked path without alternative route"""
        self.state.add_obstacle('kitchen', 'furniture', {'x': 1, 'y': 2})
        plan = [Action('navigate_to', location='kitchen')]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'blocked' in msg

    def test_validate_accepts_blocked_path_with_alternative(self):
        """Test: Accepts plan with alternative route for blocked path"""
        self.state.add_obstacle('kitchen', 'furniture', {'x': 1, 'y': 2})
        plan = [
            Action('find_alternative_route', location='kitchen'),
            Action('navigate_to', location='kitchen')
        ]

        valid, msg = self.validator.validate(plan, self.state)
        assert valid

    def test_validate_rejects_forbidden_actions(self):
        """Test: Rejects plans with forbidden actions"""
        plan = [Action('harm', target='human')]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'Forbidden' in msg

    def test_validate_rejects_empty_plan(self):
        """Test: Rejects empty plan"""
        plan = []

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'Empty' in msg

    def test_validate_rejects_too_long_plan(self):
        """Test: Rejects plan exceeding max actions"""
        plan = [Action('navigate_to', location='kitchen') for _ in range(60)]

        valid, msg = self.validator.validate(plan, self.state)
        assert not valid
        assert 'too long' in msg

    def test_should_interrupt_on_emergency(self):
        """Test: Recommends interrupting plan on emergency"""
        self.state.trigger_emergency('fire', 'kitchen')

        should_interrupt, reason = self.validator.should_interrupt_plan(self.state)
        assert should_interrupt
        assert 'Emergency' in reason

    def test_should_interrupt_on_critical_battery(self):
        """Test: Recommends interrupting on critical battery"""
        self.state.battery_level = 3.0

        should_interrupt, reason = self.validator.should_interrupt_plan(self.state)
        assert should_interrupt
        assert 'battery' in reason.lower()

    def test_should_not_interrupt_normal_conditions(self):
        """Test: Does not interrupt under normal conditions"""
        should_interrupt, reason = self.validator.should_interrupt_plan(self.state)
        assert not should_interrupt
