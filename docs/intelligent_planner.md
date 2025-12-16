# Intelligent HTN Planner

## Overview

The Hierarchical Task Network (HTN) planner provides intelligent planning for complex real-world robot scenarios. It replaces the naive symbolic planner with production-grade capabilities including:

- **Complex multi-step task decomposition**
- **Dynamic replanning on failures**
- **Conditional logic and context awareness**
- **Learning from execution history**
- **Emergency response protocols**

## Architecture

### Core Components

1. **HTNPlanner** (`brain/planner/htn_planner.py`)
   - Hierarchical task decomposition
   - Conditional logic based on world state
   - 15+ step complex task planning

2. **Replanner** (`brain/planner/replanner.py`)
   - Dynamic replanning on execution failures
   - Failure-specific recovery strategies
   - <100ms replanning performance

3. **KnowledgeBase** (`brain/planner/knowledge_base.py`)
   - Learn from failures and successes
   - Store behavioral patterns
   - Context-aware decision making

4. **ExtendedWorldState** (`brain/world/extended_state.py`)
   - Battery monitoring
   - Obstacle detection
   - Emergency condition tracking
   - Door state management

5. **EmergencySafetyValidator** (`brain/safety/emergency_rules.py`)
   - Emergency detection (fire, intrusion, fall)
   - Safety protocol enforcement
   - Plan interruption logic

## Capabilities

### 1. Complex Multi-Step Tasks

**Example: Make Coffee**
```python
from brain.planner.htn_planner import HTNPlanner
from brain.intent.schema import Goal
from brain.world.extended_state import ExtendedWorldState

planner = HTNPlanner()
state = ExtendedWorldState()
goal = Goal(action='make_coffee', target='coffee')

plan = planner.plan(goal, state)
# Generates 15+ steps:
# 1. navigate_to(kitchen)
# 2. check_power()
# 3. check_water()
# 4. check_beans()
# 5. [conditional: refill water if low]
# 6. [conditional: refill beans if low]
# 7. grind_beans()
# 8. heat_water()
# 9. brew_coffee()
# 10. grasp(coffee_cup)
# 11. navigate_to(human_location)
# 12. release(coffee_cup)
# 13. navigate_to(kitchen)
# 14. clean_machine()
```

### 2. Dynamic Replanning

**Example: Blocked Path Recovery**
```python
from brain.planner.replanner import Replanner

replanner = Replanner(base_planner)

# Original plan fails
failed_action = Action('navigate_to', location='kitchen')
failure_reason = 'path_blocked'

# Generate recovery plan
new_plan, reason = replanner.replan(
    original_goal=goal,
    failed_action=failed_action,
    failure_reason=failure_reason,
    current_state=state,
    remaining_plan=remaining_actions
)
# Returns: [find_alternative_route(kitchen), navigate_to(kitchen), ...]
```

### 3. Conditional Logic

**Example: Door Handling**
```python
# If door is closed, open it
state.set_door_state('room_305', 'closed')
goal = Goal(action='deliver_package', location='room_305')
plan = planner.plan(goal, state)
# Includes: open_door(room_305) before entering

# If door is open, skip opening
state.set_door_state('room_305', 'open')
plan = planner.plan(goal, state)
# Skips: open_door action
```

### 4. Learning from Failures

**Example: Failure Pattern Recognition**
```python
from brain.planner.knowledge_base import KnowledgeBase

kb = KnowledgeBase(persistence_path='robot_knowledge.json')

# Record failure
kb.record_failure(
    action_type='navigate_to',
    failure_reason='path_blocked',
    context={'location': 'kitchen'},
    recovery_strategy='find_alternative_route',
    recovery_successful=True
)

# Later, retrieve best recovery
recovery = kb.get_best_recovery('navigate_to', 'path_blocked')
# Returns: 'find_alternative_route' (if >50% success rate)
```

### 5. Context-Aware Decisions

**Example: Battery-Aware Planning**
```python
# Low battery triggers charging
state.battery_level = 15.0
goal = Goal(action='monitor_area', location='warehouse')
plan = planner.plan(goal, state)
# Includes: navigate_to(charging_station), charge()

# High battery skips charging
state.battery_level = 80.0
plan = planner.plan(goal, state)
# Skips charging actions
```

### 6. Emergency Response

**Example: Fire Emergency**
```python
from brain.safety.emergency_rules import EmergencySafetyValidator

validator = EmergencySafetyValidator()

# Detect emergency
state.trigger_emergency('fire', 'kitchen')
is_emergency, etype = validator.detect_emergency(state)
# Returns: (True, 'fire')

# Generate emergency plan
emergency_plan = validator.get_emergency_plan('fire', state)
# Returns: [sound_alarm(), alert_human(), call_emergency(), 
#           navigate_to_exit(), ...]
```

## Supported Scenarios

### Complex Tasks
1. **Make Coffee** - 15+ steps with conditional water/bean refill
2. **Deliver Package** - Navigation with door handling
3. **Monitor Area** - Patrol with battery management and intrusion detection
4. **Bring Object** - Enhanced with obstacle avoidance and search

### Emergency Protocols
1. **Fire** - Alarm, alert, evacuate, avoid smoke
2. **Intrusion** - Alarm, alert, record, secure
3. **Fall** - Alert, call medical, monitor vitals
4. **Critical Battery** - Emergency charging

### Failure Recovery
1. **Path Blocked** - Find alternative route
2. **Object Not Found** - Search multiple locations
3. **Object Too Heavy** - Request human assistance
4. **Door Locked** - Find key, unlock
5. **Low Battery** - Navigate to charger

## Performance

- **Planning Speed**: <100ms for typical scenarios
- **Replanning Speed**: <50ms for failure recovery
- **Memory Efficient**: Runs on embedded systems
- **Explainable**: Human-readable action sequences

## Testing

Run comprehensive test suite:
```bash
# HTN Planner tests (20+ scenarios)
pytest tests/test_htn_planner.py -v

# Replanner tests
pytest tests/test_replanner.py -v

# Knowledge base tests
pytest tests/test_knowledge_base.py -v

# Emergency safety tests
pytest tests/test_emergency_safety.py -v
```

## Integration

### Replace Existing Planner

```python
from brain.kernel import RobotBrainKernel
from brain.planner.htn_planner import HTNPlanner
from brain.planner.replanner import Replanner
from brain.planner.knowledge_base import KnowledgeBase
from brain.world.extended_state import ExtendedWorldState
from brain.safety.emergency_rules import EmergencySafetyValidator

# Create intelligent planner
htn_planner = HTNPlanner()
replanner = Replanner(htn_planner)
knowledge_base = KnowledgeBase(persistence_path='robot_kb.json')

# Use extended world state
state = ExtendedWorldState(
    robot_location='home',
    human_location='living_room',
    battery_level=80.0
)

# Use emergency safety validator
safety = EmergencySafetyValidator()

# Plan with intelligence
goal = Goal(action='make_coffee', target='coffee')
plan = htn_planner.plan(goal, state)

# Validate with emergency awareness
valid, msg = safety.validate(plan, state)

# Execute with replanning on failure
if execution_failed:
    new_plan, reason = replanner.replan(
        goal, failed_action, failure_reason, state, remaining_plan
    )
```

## Constraints

- **Offline Capable**: No external API calls
- **Fast**: <100ms planning, <50ms replanning
- **Explainable**: Human-readable plans
- **Memory Efficient**: Suitable for embedded systems
- **Graceful Degradation**: Partial success over total failure

## Future Extensions

- PDDL-style formal planning language
- Parallel action execution
- Probabilistic planning under uncertainty
- Multi-robot coordination
- Natural language plan explanation

## References

- HTN Planning: Erol, K., Hendler, J., & Nau, D. S. (1994). "HTN Planning: Complexity and Expressivity"
- Replanning: Fox, M., & Long, D. (2003). "PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains"
- Learning: Veloso, M. (1994). "Planning and Learning by Analogical Reasoning"
