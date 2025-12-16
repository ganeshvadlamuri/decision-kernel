"""Emergency detection and safety rules for critical situations"""
from brain.planner.actions import Action
from brain.world.extended_state import ExtendedWorldState


class EmergencySafetyValidator:
    """Validate plans and detect emergency situations"""

    def __init__(self):
        self.max_actions = 50  # Increased for complex scenarios
        self.forbidden_actions = ['harm', 'damage', 'ignore_emergency']
        self.emergency_protocols = {
            'fire': self._fire_protocol,
            'intrusion': self._intrusion_protocol,
            'fall': self._fall_protocol,
            'low_battery_critical': self._critical_battery_protocol
        }

    def validate(self, plan: list[Action], state: ExtendedWorldState) -> tuple[bool, str]:
        """Validate plan with emergency awareness"""

        # Check for emergencies first
        if state.has_emergency():
            emergency_type = state.get_emergency_type()
            return False, f"EMERGENCY: {emergency_type} detected - override plan required"

        # Check critical battery
        if state.battery_level < 5.0 and not self._plan_includes_charging(plan):
            return False, "CRITICAL: Battery too low, must charge immediately"

        # Basic validation
        if len(plan) == 0:
            return False, "Empty plan"

        if len(plan) > self.max_actions:
            return False, f"Plan too long ({len(plan)} > {self.max_actions})"

        # Check forbidden actions
        for action in plan:
            if action.action_type in self.forbidden_actions:
                return False, f"Forbidden action: {action.action_type}"

        # Check battery sufficiency
        estimated_battery_use = len(plan) * 2.0  # 2% per action estimate
        if state.battery_level < estimated_battery_use:
            return False, f"Insufficient battery for plan (need {estimated_battery_use}%, have {state.battery_level}%)"

        # Check for navigation to blocked paths
        for action in plan:
            if action.action_type == 'navigate_to' and action.location:
                if state.is_path_blocked(action.location):
                    if not self._plan_includes_alternative_route(plan, action.location):
                        return False, f"Path to {action.location} is blocked, no alternative route in plan"

        return True, "PASS"

    def detect_emergency(self, state: ExtendedWorldState) -> tuple[bool, str | None]:
        """Detect emergency conditions from world state"""

        # Fire detection
        if state.fire_detected:
            return True, 'fire'

        # Intrusion detection
        if state.intrusion_detected:
            return True, 'intrusion'

        # Fall detection
        if state.fall_detected:
            return True, 'fall'

        # Critical battery
        if state.battery_level < 5.0 and not state.charging:
            return True, 'low_battery_critical'

        # Temperature extreme
        if state.temperature > 40.0 or state.temperature < 0.0:
            return True, 'temperature_extreme'

        return False, None

    def get_emergency_plan(self, emergency_type: str, state: ExtendedWorldState) -> list[Action]:
        """Generate emergency response plan"""
        if emergency_type in self.emergency_protocols:
            return self.emergency_protocols[emergency_type](state)
        return []

    def _fire_protocol(self, state: ExtendedWorldState) -> list[Action]:
        """Fire emergency protocol"""
        return [
            Action('sound_alarm', parameters={'type': 'fire'}),
            Action('alert_human', parameters={'message': 'FIRE_DETECTED', 'location': state.fire_location}),
            Action('call_emergency', parameters={'service': '911', 'type': 'fire'}),
            Action('close_door', location=state.fire_location) if state.fire_location else Action('stop'),
            Action('avoid_area', location=state.fire_location) if state.fire_location else Action('stop'),
            Action('navigate_to_exit', parameters={'priority': 'emergency'}),
            Action('alert_human', parameters={'message': 'EVACUATE_NOW'})
        ]

    def _intrusion_protocol(self, state: ExtendedWorldState) -> list[Action]:
        """Intrusion emergency protocol"""
        actions = [
            Action('sound_alarm', parameters={'type': 'intrusion'}),
            Action('alert_human', parameters={'message': 'INTRUSION_DETECTED', 'location': state.intrusion_location}),
            Action('call_emergency', parameters={'service': '911', 'type': 'intrusion'})
        ]
        if state.intrusion_location:
            actions.append(Action('record_video', location=state.intrusion_location))
        actions.extend([
            Action('navigate_to', location='safe_room'),
            Action('lock_door', location='safe_room')
        ])
        return actions

    def _fall_protocol(self, state: ExtendedWorldState) -> list[Action]:
        """Fall detection emergency protocol"""
        return [
            Action('alert_human', parameters={'message': 'FALL_DETECTED'}),
            Action('call_emergency', parameters={'service': '911', 'type': 'medical'}),
            Action('navigate_to', location=state.human_location),
            Action('monitor_vital_signs', parameters={'continuous': True}),
            Action('wait_for_emergency_services', parameters={})
        ]

    def _critical_battery_protocol(self, state: ExtendedWorldState) -> list[Action]:
        """Critical battery emergency protocol"""
        return [
            Action('alert_human', parameters={'message': 'CRITICAL_BATTERY'}),
            Action('stop_all_operations', parameters={}),
            Action('navigate_to', location='charging_station'),
            Action('charge', parameters={'priority': 'emergency'})
        ]

    def _plan_includes_charging(self, plan: list[Action]) -> bool:
        """Check if plan includes charging action"""
        return any(action.action_type == 'charge' for action in plan)

    def _plan_includes_alternative_route(self, plan: list[Action], location: str) -> bool:
        """Check if plan includes finding alternative route"""
        return any(
            action.action_type == 'find_alternative_route' and action.location == location
            for action in plan
        )

    def should_interrupt_plan(self, state: ExtendedWorldState) -> tuple[bool, str]:
        """Check if current plan should be interrupted"""

        # Emergency detected
        if state.has_emergency():
            return True, f"Emergency: {state.get_emergency_type()}"

        # Critical battery
        if state.battery_level < 5.0:
            return True, "Critical battery level"

        # Human in danger (based on context)
        if state.human_present and state.fire_detected:
            return True, "Human safety at risk"

        return False, ""
