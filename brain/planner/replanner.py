"""Dynamic replanning for handling execution failures and obstacles"""
from dataclasses import dataclass
from typing import Callable
from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.world.state import WorldState
from brain.planner.htn_planner import HTNPlanner


@dataclass
class ExecutionFailure:
    """Record of failed action execution"""
    action: Action
    reason: str
    state_snapshot: WorldState
    timestamp: float


class Replanner:
    """Dynamic replanner that adapts to execution failures"""
    
    def __init__(self, base_planner: HTNPlanner):
        self.base_planner = base_planner
        self.failure_handlers: dict[str, Callable] = {}
        self._register_handlers()
    
    def replan(
        self,
        original_goal: Goal,
        failed_action: Action,
        failure_reason: str,
        current_state: WorldState,
        remaining_plan: list[Action]
    ) -> tuple[list[Action], str]:
        """Generate new plan after failure"""
        
        # Try specific failure handler
        handler_key = f"{failed_action.action_type}_{failure_reason}"
        if handler_key in self.failure_handlers:
            new_actions = self.failure_handlers[handler_key](
                failed_action, current_state, original_goal
            )
            if new_actions:
                return new_actions + remaining_plan, f"Recovered using {handler_key}"
        
        # Try generic action handler
        if failed_action.action_type in self.failure_handlers:
            new_actions = self.failure_handlers[failed_action.action_type](
                failed_action, current_state, original_goal
            )
            if new_actions:
                return new_actions + remaining_plan, f"Recovered using generic handler"
        
        # Full replan from current state
        new_plan = self.base_planner.plan(original_goal, current_state)
        if new_plan:
            return new_plan, "Full replan from current state"
        
        return [], "No recovery strategy found"
    
    def _register_handlers(self):
        """Register failure recovery strategies"""
        
        # Navigation failures
        self.failure_handlers['navigate_to_path_blocked'] = self._handle_blocked_path
        self.failure_handlers['navigate_to_obstacle'] = self._handle_obstacle
        
        # Grasp failures
        self.failure_handlers['grasp_object_not_found'] = self._handle_object_not_found
        self.failure_handlers['grasp_object_too_heavy'] = self._handle_heavy_object
        
        # Door failures
        self.failure_handlers['open_door_locked'] = self._handle_locked_door
        
        # Battery failures
        self.failure_handlers['navigate_to_low_battery'] = self._handle_low_battery
        
        # Generic handlers
        self.failure_handlers['navigate_to'] = self._handle_navigation_generic
        self.failure_handlers['grasp'] = self._handle_grasp_generic
    
    def _handle_blocked_path(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle blocked navigation path"""
        return [
            Action('find_alternative_route', location=action.location),
            Action('navigate_to', location=action.location)
        ]
    
    def _handle_obstacle(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle unexpected obstacle"""
        return [
            Action('detect_obstacle', location=action.location),
            Action('avoid_obstacle', location=action.location),
            Action('navigate_to', location=action.location)
        ]
    
    def _handle_object_not_found(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle missing object - search common locations"""
        search_locations = ['kitchen', 'living_room', 'bedroom', 'storage']
        actions = []
        
        for loc in search_locations:
            actions.append(Action('navigate_to', location=loc))
            actions.append(Action('search_area', location=loc, target=action.target))
        
        actions.append(Action('grasp', target=action.target))
        return actions
    
    def _handle_heavy_object(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle object too heavy - get help or use tool"""
        return [
            Action('alert_human', parameters={'message': 'need_assistance', 'object': action.target}),
            Action('wait_for_human', parameters={'timeout': 60}),
            Action('grasp', target=action.target, parameters={'assisted': True})
        ]
    
    def _handle_locked_door(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle locked door - find key or alternative route"""
        return [
            Action('search_for_key', location=action.location),
            Action('grasp', target='key'),
            Action('unlock_door', location=action.location),
            Action('open_door', location=action.location)
        ]
    
    def _handle_low_battery(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Handle low battery during navigation"""
        return [
            Action('navigate_to', location='charging_station'),
            Action('charge', parameters={'duration': 300}),
            Action('navigate_to', location=action.location)
        ]
    
    def _handle_navigation_generic(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Generic navigation failure handler"""
        return [
            Action('stop', parameters={}),
            Action('wait', parameters={'duration': 2}),
            Action('navigate_to', location=action.location)
        ]
    
    def _handle_grasp_generic(self, action: Action, state: WorldState, goal: Goal) -> list[Action]:
        """Generic grasp failure handler"""
        return [
            Action('release', target=action.target),
            Action('reposition', parameters={}),
            Action('grasp', target=action.target)
        ]
