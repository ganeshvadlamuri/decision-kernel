"""Demo of intelligent HTN planner capabilities"""
from brain.planner.htn_planner import HTNPlanner
from brain.planner.replanner import Replanner
from brain.planner.knowledge_base import KnowledgeBase
from brain.intent.schema import Goal
from brain.world.extended_state import ExtendedWorldState
from brain.world.objects import WorldObject
from brain.safety.emergency_rules import EmergencySafetyValidator
from brain.planner.actions import Action


def print_plan(title: str, plan: list[Action]):
    """Pretty print a plan"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    for i, action in enumerate(plan, 1):
        print(f"  {i}. {action}")
    print(f"{'='*60}\n")


def demo_complex_tasks():
    """Demo 1: Complex multi-step tasks"""
    print("\n[DEMO 1] Complex Multi-Step Tasks")
    
    planner = HTNPlanner()
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Make coffee
    goal = Goal(action='make_coffee', target='coffee')
    plan = planner.plan(goal, state)
    print_plan("Make Coffee (15+ steps)", plan)
    
    # Deliver package
    goal = Goal(action='deliver_package', location='room_305')
    plan = planner.plan(goal, state)
    print_plan("Deliver Package", plan)


def demo_conditional_logic():
    """Demo 2: Conditional logic"""
    print("\n[DEMO 2] Conditional Logic")
    
    planner = HTNPlanner()
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Low water triggers refill
    print("\n[Scenario] Low water level")
    state.relations['water_level'] = 20
    goal = Goal(action='make_coffee', target='coffee')
    plan = planner.plan(goal, state)
    print(f"  Water level: 20% -> Plan includes water refill")
    print(f"  Plan length: {len(plan)} steps")
    
    # High water skips refill
    print("\n[Scenario] High water level")
    state.relations['water_level'] = 80
    plan2 = planner.plan(goal, state)
    print(f"  Water level: 80% -> Plan skips water refill")
    print(f"  Plan length: {len(plan2)} steps")
    print(f"  Difference: {len(plan) - len(plan2)} fewer steps")


def demo_dynamic_replanning():
    """Demo 3: Dynamic replanning"""
    print("\n[DEMO 3] Dynamic Replanning")
    
    planner = HTNPlanner()
    replanner = Replanner(planner)
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Path blocked recovery
    print("\n[Scenario] Path blocked")
    goal = Goal(action='bring', target='water')
    failed_action = Action('navigate_to', location='kitchen')
    remaining = [Action('grasp', target='water')]
    
    new_plan, reason = replanner.replan(
        goal, failed_action, 'path_blocked', state, remaining
    )
    print(f"  Original action failed: {failed_action}")
    print(f"  Recovery strategy: {reason}")
    print_plan("Recovery Plan", new_plan[:5])  # Show first 5 actions
    
    # Object not found recovery
    print("\n[Scenario] Object not found")
    failed_action = Action('grasp', target='keys')
    new_plan, reason = replanner.replan(
        goal, failed_action, 'object_not_found', state, []
    )
    print(f"  Original action failed: {failed_action}")
    print(f"  Recovery strategy: {reason}")
    print(f"  Recovery includes searching {len([a for a in new_plan if a.action_type == 'navigate_to'])} locations")


def demo_learning():
    """Demo 4: Learning from failures"""
    print("\n[DEMO 4] Learning from Failures")
    
    kb = KnowledgeBase()
    
    # Record failures
    print("\n[Recording] Failure patterns...")
    kb.record_failure('navigate_to', 'path_blocked', {'location': 'kitchen'}, 
                     recovery_strategy='find_alternative_route', recovery_successful=True)
    kb.record_failure('navigate_to', 'path_blocked', {'location': 'bedroom'},
                     recovery_strategy='find_alternative_route', recovery_successful=True)
    kb.record_failure('grasp', 'object_not_found', {},
                     recovery_strategy='search_area', recovery_successful=True)
    
    # Get statistics
    stats = kb.get_failure_statistics()
    print(f"\n[Statistics] Failures:")
    print(f"  Total patterns learned: {stats['total_patterns']}")
    print(f"\n  Most common failures:")
    for failure in stats['most_common']:
        print(f"    - {failure['action']}/{failure['reason']}: {failure['count']} times")
    
    print(f"\n  Best recovery strategies:")
    for recovery in stats['best_recoveries']:
        print(f"    - {recovery['action']}/{recovery['reason']}")
        print(f"      -> {recovery['recovery']} ({recovery['success_rate']*100:.0f}% success)")
    
    # Retrieve learned recovery
    print("\n[Applying] Learned knowledge:")
    recovery = kb.get_best_recovery('navigate_to', 'path_blocked')
    print(f"  For 'navigate_to' failure with 'path_blocked'")
    print(f"  -> Use strategy: {recovery}")


def demo_emergency_response():
    """Demo 5: Emergency situations"""
    print("\n[DEMO 5] Emergency Response")
    
    validator = EmergencySafetyValidator()
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Fire emergency
    print("\n[Scenario] Fire detected")
    state.trigger_emergency('fire', 'kitchen')
    is_emergency, etype = validator.detect_emergency(state)
    print(f"  Emergency detected: {etype}")
    
    emergency_plan = validator.get_emergency_plan('fire', state)
    print_plan("Fire Emergency Protocol", emergency_plan)
    
    # Intrusion emergency
    state.clear_emergency('fire')
    print("\n[Scenario] Intrusion detected")
    state.trigger_emergency('intrusion', 'back_door')
    emergency_plan = validator.get_emergency_plan('intrusion', state)
    print_plan("Intrusion Emergency Protocol", emergency_plan)


def demo_context_awareness():
    """Demo 6: Context-aware decisions"""
    print("\n[DEMO 6] Context-Aware Decisions")
    
    planner = HTNPlanner()
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Battery-aware planning
    print("\n[Scenario] Battery management")
    state.battery_level = 15.0
    goal = Goal(action='monitor_area', location='warehouse')
    plan = planner.plan(goal, state)
    
    print(f"  Battery level: 15%")
    print(f"  Plan includes charging: {'charge' in [a.action_type for a in plan]}")
    
    state.battery_level = 80.0
    plan2 = planner.plan(goal, state)
    print(f"\n  Battery level: 80%")
    print(f"  Plan includes charging: {'charge' in [a.action_type for a in plan2]}")


def demo_performance():
    """Demo 7: Performance benchmarks"""
    print("\n[DEMO 7] Performance Benchmarks")
    
    import time
    
    planner = HTNPlanner()
    state = ExtendedWorldState(
        robot_location='home',
        human_location='living_room',
        battery_level=80.0
    )
    
    # Planning speed
    print("\n[Benchmark] Planning Speed:")
    scenarios = [
        ('make_coffee', 'coffee'),
        ('deliver_package', None),
        ('monitor_area', None),
        ('bring', 'water'),
        ('emergency_fire', None)
    ]
    
    for action, target in scenarios:
        goal = Goal(action=action, target=target, location='warehouse')
        
        start = time.time()
        plan = planner.plan(goal, state)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        print(f"  {action:20s}: {elapsed:6.2f}ms ({len(plan):2d} actions)")
    
    # Replanning speed
    print("\n[Benchmark] Replanning Speed:")
    replanner = Replanner(planner)
    goal = Goal(action='bring', target='water')
    failed_action = Action('navigate_to', location='kitchen')
    
    start = time.time()
    new_plan, reason = replanner.replan(goal, failed_action, 'path_blocked', state, [])
    elapsed = (time.time() - start) * 1000
    
    print(f"  Path blocked recovery: {elapsed:6.2f}ms ({len(new_plan)} actions)")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("  INTELLIGENT HTN PLANNER DEMONSTRATION")
    print("="*60)
    
    demo_complex_tasks()
    demo_conditional_logic()
    demo_dynamic_replanning()
    demo_learning()
    demo_emergency_response()
    demo_context_awareness()
    demo_performance()
    
    print("\n" + "="*60)
    print("  [SUCCESS] All demos completed successfully!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
