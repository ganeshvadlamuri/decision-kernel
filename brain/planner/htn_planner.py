"""Hierarchical Task Network (HTN) Planner for complex real-world scenarios"""
from dataclasses import dataclass, field
from typing import Callable
from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.world.state import WorldState


@dataclass
class Precondition:
    """Condition that must be true before action execution"""
    check: Callable[[WorldState], bool]
    description: str


@dataclass
class Effect:
    """State change after action execution"""
    apply: Callable[[WorldState], None]
    description: str


@dataclass
class EnhancedAction(Action):
    """Action with preconditions and effects"""
    preconditions: list[Precondition] = field(default_factory=list)
    effects: list[Effect] = field(default_factory=list)
    cost: float = 1.0
    
    def can_execute(self, state: WorldState) -> tuple[bool, str]:
        for pre in self.preconditions:
            if not pre.check(state):
                return False, f"Precondition failed: {pre.description}"
        return True, "OK"


@dataclass
class Task:
    """High-level task that decomposes into subtasks or actions"""
    name: str
    decompositions: list[Callable[[WorldState, dict], list]] = field(default_factory=list)
    is_primitive: bool = False
    
    def decompose(self, state: WorldState, params: dict) -> list:
        """Try decompositions until one succeeds"""
        for decomp in self.decompositions:
            try:
                result = decomp(state, params)
                if result:
                    return result
            except Exception:
                continue
        return []


class HTNPlanner:
    """Hierarchical Task Network planner with conditional logic"""
    
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self._register_tasks()
    
    def plan(self, goal: Goal, state: WorldState) -> list[Action]:
        """Generate plan using HTN decomposition"""
        task_name = goal.action
        params = {
            'target': goal.target,
            'location': goal.location,
            'recipient': getattr(goal, 'recipient', None)
        }
        
        if task_name not in self.tasks:
            return []
        
        return self._decompose_recursive(task_name, state, params)
    
    def _decompose_recursive(self, task_name: str, state: WorldState, params: dict) -> list[Action]:
        """Recursively decompose tasks into primitive actions"""
        if task_name not in self.tasks:
            return []
        
        task = self.tasks[task_name]
        
        if task.is_primitive:
            return [self._create_action(task_name, params)]
        
        subtasks = task.decompose(state, params)
        actions = []
        
        for subtask in subtasks:
            if isinstance(subtask, str):
                actions.extend(self._decompose_recursive(subtask, state, params))
            elif isinstance(subtask, dict):
                sub_name = subtask.get('task')
                sub_params = {**params, **subtask.get('params', {})}
                actions.extend(self._decompose_recursive(sub_name, state, sub_params))
        
        return actions
    
    def _create_action(self, action_type: str, params: dict) -> Action:
        """Create action from task and parameters"""
        return Action(
            action_type=action_type,
            target=params.get('target'),
            location=params.get('location'),
            parameters={k: v for k, v in params.items() if k not in ['target', 'location']}
        )
    
    def _register_tasks(self):
        """Register all task decompositions"""
        
        # COMPLEX TASK: Make Coffee
        self.tasks['make_coffee'] = Task(
            name='make_coffee',
            decompositions=[self._decompose_make_coffee]
        )
        
        # COMPLEX TASK: Deliver Package
        self.tasks['deliver_package'] = Task(
            name='deliver_package',
            decompositions=[self._decompose_deliver_package]
        )
        
        # COMPLEX TASK: Monitor Area
        self.tasks['monitor_area'] = Task(
            name='monitor_area',
            decompositions=[self._decompose_monitor_area]
        )
        
        # COMPLEX TASK: Bring Object (enhanced)
        self.tasks['bring'] = Task(
            name='bring',
            decompositions=[self._decompose_bring]
        )
        
        # COMPLEX TASK: Emergency Response
        self.tasks['emergency_fire'] = Task(
            name='emergency_fire',
            decompositions=[self._decompose_emergency_fire]
        )
        
        # PRIMITIVE ACTIONS
        primitives = [
            'navigate_to', 'grasp', 'release', 'open_door', 'close_door',
            'check_water', 'check_beans', 'check_power', 'grind_beans',
            'heat_water', 'brew_coffee', 'clean_machine', 'verify_id',
            'scan_barcode', 'knock_door', 'find_alternative_route',
            'patrol', 'check_battery', 'charge', 'alert_human',
            'detect_intrusion', 'sound_alarm', 'navigate_to_exit',
            'avoid_area', 'call_emergency'
        ]
        
        for prim in primitives:
            self.tasks[prim] = Task(name=prim, is_primitive=True)
    
    def _decompose_make_coffee(self, state: WorldState, params: dict) -> list:
        """Decompose make_coffee into 15+ steps"""
        return [
            {'task': 'navigate_to', 'params': {'location': 'kitchen'}},
            {'task': 'check_power', 'params': {}},
            {'task': 'check_water', 'params': {}},
            {'task': 'check_beans', 'params': {}},
            # Conditional: if water low, refill
            *self._conditional_refill_water(state),
            # Conditional: if beans low, refill
            *self._conditional_refill_beans(state),
            {'task': 'grind_beans', 'params': {}},
            {'task': 'heat_water', 'params': {}},
            {'task': 'brew_coffee', 'params': {}},
            {'task': 'grasp', 'params': {'target': 'coffee_cup'}},
            {'task': 'navigate_to', 'params': {'location': state.human_location}},
            {'task': 'release', 'params': {'target': 'coffee_cup'}},
            {'task': 'navigate_to', 'params': {'location': 'kitchen'}},
            {'task': 'clean_machine', 'params': {}}
        ]
    
    def _decompose_deliver_package(self, state: WorldState, params: dict) -> list:
        """Decompose package delivery with door handling"""
        target_room = params.get('location', 'room_305')
        
        return [
            {'task': 'grasp', 'params': {'target': 'package'}},
            {'task': 'navigate_to', 'params': {'location': target_room}},
            # Conditional: if door closed, handle it
            *self._conditional_open_door(state, target_room),
            {'task': 'knock_door', 'params': {}},
            {'task': 'release', 'params': {'target': 'package'}}
        ]
    
    def _decompose_monitor_area(self, state: WorldState, params: dict) -> list:
        """Decompose monitoring with battery management"""
        return [
            {'task': 'patrol', 'params': {'location': params.get('location', 'warehouse')}},
            {'task': 'check_battery', 'params': {}},
            # Conditional: if battery low, charge
            *self._conditional_charge(state),
            {'task': 'detect_intrusion', 'params': {}},
            # Conditional: if intrusion, alert
            *self._conditional_alert_intrusion(state)
        ]
    
    def _decompose_bring(self, state: WorldState, params: dict) -> list:
        """Enhanced bring with obstacle handling"""
        target = params.get('target', 'unknown')
        obj = state.get_object(target)
        object_location = obj.location if obj else 'kitchen'
        
        return [
            {'task': 'navigate_to', 'params': {'location': object_location}},
            # Conditional: if path blocked, find alternative
            *self._conditional_alternative_route(state, object_location),
            # Conditional: if object not found, search
            *self._conditional_search_object(state, target),
            {'task': 'grasp', 'params': {'target': target}},
            {'task': 'navigate_to', 'params': {'location': state.human_location}},
            {'task': 'release', 'params': {'target': target}}
        ]
    
    def _decompose_emergency_fire(self, state: WorldState, params: dict) -> list:
        """Emergency fire response protocol"""
        return [
            {'task': 'sound_alarm', 'params': {}},
            {'task': 'alert_human', 'params': {'message': 'FIRE_DETECTED'}},
            {'task': 'call_emergency', 'params': {'service': '911'}},
            {'task': 'avoid_area', 'params': {'location': 'fire_zone'}},
            {'task': 'navigate_to_exit', 'params': {}},
            {'task': 'alert_human', 'params': {'message': 'EVACUATE'}}
        ]
    
    # CONDITIONAL LOGIC HELPERS
    
    def _conditional_refill_water(self, state: WorldState) -> list:
        """Add water refill if needed"""
        water_level = state.relations.get('water_level', 100)
        if water_level < 30:
            return [
                {'task': 'navigate_to', 'params': {'location': 'sink'}},
                {'task': 'grasp', 'params': {'target': 'water_container'}},
                {'task': 'release', 'params': {'target': 'water_container'}}
            ]
        return []
    
    def _conditional_refill_beans(self, state: WorldState) -> list:
        """Add bean refill if needed"""
        bean_level = state.relations.get('bean_level', 100)
        if bean_level < 20:
            return [
                {'task': 'grasp', 'params': {'target': 'bean_bag'}},
                {'task': 'release', 'params': {'target': 'bean_container'}}
            ]
        return []
    
    def _conditional_open_door(self, state: WorldState, location: str) -> list:
        """Open door if closed"""
        door_state = state.relations.get(f'{location}_door', 'closed')
        if door_state == 'closed':
            return [{'task': 'open_door', 'params': {'location': location}}]
        return []
    
    def _conditional_charge(self, state: WorldState) -> list:
        """Charge if battery low"""
        battery = state.relations.get('battery_level', 100)
        if battery < 20:
            return [
                {'task': 'navigate_to', 'params': {'location': 'charging_station'}},
                {'task': 'charge', 'params': {}}
            ]
        return []
    
    def _conditional_alert_intrusion(self, state: WorldState) -> list:
        """Alert if intrusion detected"""
        intrusion = state.relations.get('intrusion_detected', False)
        if intrusion:
            return [
                {'task': 'alert_human', 'params': {'message': 'INTRUSION'}},
                {'task': 'sound_alarm', 'params': {}}
            ]
        return []
    
    def _conditional_alternative_route(self, state: WorldState, location: str) -> list:
        """Find alternative route if path blocked"""
        path_blocked = state.relations.get(f'path_to_{location}_blocked', False)
        if path_blocked:
            return [{'task': 'find_alternative_route', 'params': {'location': location}}]
        return []
    
    def _conditional_search_object(self, state: WorldState, target: str) -> list:
        """Search for object if not found"""
        obj = state.get_object(target)
        if not obj:
            return [
                {'task': 'navigate_to', 'params': {'location': 'storage'}},
                {'task': 'navigate_to', 'params': {'location': 'kitchen'}},
                {'task': 'navigate_to', 'params': {'location': 'living_room'}}
            ]
        return []
