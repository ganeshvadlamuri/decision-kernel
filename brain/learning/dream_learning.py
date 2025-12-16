"""Dream-Based Learning - Robot improves while charging through simulation"""
import random
import time
from dataclasses import dataclass
from typing import Any

from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.world.state import WorldState


@dataclass
class DreamScenario:
    """Simulated scenario for dream learning"""
    goal: Goal
    initial_state: WorldState
    difficulty: float  # 0.0 to 1.0
    scenario_type: str
    constraints: dict[str, Any]


@dataclass
class DreamOutcome:
    """Result of dream simulation"""
    scenario: DreamScenario
    plan: list[Action]
    success: bool
    lessons_learned: list[str]
    skill_improvements: dict[str, float]
    duration: float


class DreamLearningEngine:
    """Learns by simulating scenarios during idle/charging time"""
    
    def __init__(self, base_planner, knowledge_base):
        self.base_planner = base_planner
        self.knowledge_base = knowledge_base
        self.dream_history: list[DreamOutcome] = []
        self.skill_levels: dict[str, float] = {}
        self.is_dreaming = False
        self.dreams_per_session = 100
        
    def start_dreaming(self, duration_minutes: float = 60):
        """Start dream learning session (during charging)"""
        self.is_dreaming = True
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        dream_count = 0
        
        print(f"[DREAMING] Starting {duration_minutes}min dream session...")
        
        while time.time() < end_time and dream_count < self.dreams_per_session:
            # Generate random scenario
            scenario = self._generate_dream_scenario()
            
            # Simulate execution
            outcome = self._simulate_dream(scenario)
            
            # Learn from outcome
            self._learn_from_dream(outcome)
            
            self.dream_history.append(outcome)
            dream_count += 1
            
            # Brief pause between dreams
            time.sleep(0.01)
        
        self.is_dreaming = False
        
        return self._generate_dream_report(dream_count)
    
    def _generate_dream_scenario(self) -> DreamScenario:
        """Generate random scenario to practice"""
        # Random goal types
        goal_types = [
            'bring', 'make_coffee', 'deliver_package', 
            'monitor_area', 'navigate_to', 'emergency_fire'
        ]
        
        # Random difficulty based on past failures
        difficulty = random.uniform(0.3, 1.0)
        
        # Create scenario
        goal_type = random.choice(goal_types)
        
        # Generate challenging state
        state = self._generate_challenging_state(difficulty)
        
        goal = Goal(
            action=goal_type,
            target=random.choice(['water', 'cup', 'package', 'coffee']),
            location=random.choice(['kitchen', 'bedroom', 'warehouse'])
        )
        
        return DreamScenario(
            goal=goal,
            initial_state=state,
            difficulty=difficulty,
            scenario_type=goal_type,
            constraints=self._generate_constraints(difficulty)
        )
    
    def _generate_challenging_state(self, difficulty: float) -> WorldState:
        """Generate world state with challenges based on difficulty"""
        state = WorldState()
        
        # Add challenges based on difficulty
        if difficulty > 0.5:
            state.relations['battery_level'] = random.uniform(10, 30)
        
        if difficulty > 0.6:
            state.relations['path_to_kitchen_blocked'] = True
        
        if difficulty > 0.7:
            state.relations['water_level'] = random.uniform(0, 20)
        
        if difficulty > 0.8:
            state.relations['intrusion_detected'] = True
        
        return state
    
    def _generate_constraints(self, difficulty: float) -> dict[str, Any]:
        """Generate constraints for scenario"""
        return {
            'max_duration': 60 / difficulty,  # Less time for harder scenarios
            'max_actions': int(20 / difficulty),
            'battery_constraint': difficulty > 0.5,
            'obstacle_probability': difficulty * 0.5
        }
    
    def _simulate_dream(self, scenario: DreamScenario) -> DreamOutcome:
        """Simulate scenario execution"""
        start = time.time()
        
        # Generate plan
        plan = self.base_planner.plan(scenario.goal, scenario.initial_state)
        
        # Simulate execution with random failures
        success = True
        lessons = []
        skill_improvements = {}
        
        for i, action in enumerate(plan):
            # Simulate action with failure probability
            failure_prob = scenario.difficulty * 0.3
            
            if random.random() < failure_prob:
                success = False
                lessons.append(f"Action {action.action_type} failed at step {i}")
                
                # Learn recovery strategy
                recovery = self._practice_recovery(action, scenario.initial_state)
                if recovery:
                    lessons.append(f"Learned recovery: {recovery}")
                break
        
        # Update skill levels
        skill_improvements = self._calculate_skill_improvements(
            scenario, success, len(plan)
        )
        
        duration = time.time() - start
        
        return DreamOutcome(
            scenario=scenario,
            plan=plan,
            success=success,
            lessons_learned=lessons,
            skill_improvements=skill_improvements,
            duration=duration
        )
    
    def _practice_recovery(self, failed_action: Action, state: WorldState) -> str | None:
        """Practice recovery from failure"""
        recovery_strategies = {
            'navigate_to': 'find_alternative_route',
            'grasp': 'search_area',
            'open_door': 'check_door_state'
        }
        
        return recovery_strategies.get(failed_action.action_type)
    
    def _calculate_skill_improvements(
        self, 
        scenario: DreamScenario, 
        success: bool, 
        plan_length: int
    ) -> dict[str, float]:
        """Calculate skill improvements from dream"""
        improvements = {}
        
        skill_name = scenario.scenario_type
        
        # Improvement based on success and difficulty
        if success:
            improvement = scenario.difficulty * 0.1
        else:
            improvement = scenario.difficulty * 0.05  # Still learn from failure
        
        # Update skill level
        current_level = self.skill_levels.get(skill_name, 0.0)
        new_level = min(current_level + improvement, 1.0)
        self.skill_levels[skill_name] = new_level
        
        improvements[skill_name] = improvement
        
        return improvements
    
    def _learn_from_dream(self, outcome: DreamOutcome):
        """Extract and store lessons from dream"""
        # Record in knowledge base
        if not outcome.success:
            for lesson in outcome.lessons_learned:
                if 'failed' in lesson:
                    # Extract failure info and record
                    action_type = outcome.plan[0].action_type if outcome.plan else 'unknown'
                    self.knowledge_base.record_failure(
                        action_type=action_type,
                        failure_reason='dream_simulation',
                        context={'difficulty': outcome.scenario.difficulty},
                        recovery_strategy=None,
                        recovery_successful=False
                    )
    
    def _generate_dream_report(self, dream_count: int) -> dict[str, Any]:
        """Generate report of dream session"""
        recent_dreams = self.dream_history[-dream_count:]
        
        success_rate = sum(1 for d in recent_dreams if d.success) / len(recent_dreams)
        avg_difficulty = sum(d.scenario.difficulty for d in recent_dreams) / len(recent_dreams)
        
        total_lessons = sum(len(d.lessons_learned) for d in recent_dreams)
        
        return {
            'dreams_completed': dream_count,
            'success_rate': success_rate,
            'avg_difficulty': avg_difficulty,
            'lessons_learned': total_lessons,
            'skill_improvements': dict(self.skill_levels),
            'total_dream_time': sum(d.duration for d in recent_dreams)
        }
    
    def get_skill_level(self, skill_name: str) -> float:
        """Get current skill level (0.0 to 1.0)"""
        return self.skill_levels.get(skill_name, 0.0)
    
    def get_dream_statistics(self) -> dict[str, Any]:
        """Get statistics about dream learning"""
        if not self.dream_history:
            return {'total_dreams': 0}
        
        return {
            'total_dreams': len(self.dream_history),
            'success_rate': sum(1 for d in self.dream_history if d.success) / len(self.dream_history),
            'avg_difficulty': sum(d.scenario.difficulty for d in self.dream_history) / len(self.dream_history),
            'total_lessons': sum(len(d.lessons_learned) for d in self.dream_history),
            'skill_levels': dict(self.skill_levels)
        }
