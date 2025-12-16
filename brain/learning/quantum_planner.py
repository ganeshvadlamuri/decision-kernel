"""Quantum Superposition Planning - Explore multiple futures simultaneously"""
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

from brain.intent.schema import Goal
from brain.planner.actions import Action
from brain.world.state import WorldState


@dataclass
class PlanOutcome:
    """Outcome of a simulated plan execution"""
    plan: list[Action]
    success_probability: float
    expected_duration: float
    risk_score: float
    failure_points: list[int]
    alternate_paths: list[list[Action]]


@dataclass
class QuantumState:
    """Superposition of multiple possible world states"""
    states: list[WorldState]
    probabilities: list[float]
    
    def collapse(self) -> WorldState:
        """Collapse superposition to single most likely state"""
        max_prob_idx = self.probabilities.index(max(self.probabilities))
        return self.states[max_prob_idx]


class QuantumPlanner:
    """Plans by simulating multiple futures in parallel"""
    
    def __init__(self, base_planner, max_workers: int = 4):
        self.base_planner = base_planner
        self.max_workers = max_workers
    
    def superposition_plan(
        self,
        goal: Goal,
        state: WorldState,
        futures: int = 1000,
        simulation_depth: int = 10
    ) -> PlanOutcome:
        """Generate plan by exploring multiple possible futures"""
        
        # Generate base plan
        base_plan = self.base_planner.plan(goal, state)
        if not base_plan:
            return PlanOutcome([], 0.0, 0.0, 1.0, [], [])
        
        # Simulate plan execution across multiple futures
        outcomes = self._simulate_futures(base_plan, state, futures, simulation_depth)
        
        # Analyze outcomes
        success_prob = sum(1 for o in outcomes if o['success']) / len(outcomes)
        avg_duration = sum(o['duration'] for o in outcomes) / len(outcomes)
        risk_score = self._calculate_risk(outcomes)
        failure_points = self._identify_failure_points(outcomes)
        
        # Generate alternate paths for high-risk points
        alternate_paths = self._generate_alternates(base_plan, failure_points, state)
        
        return PlanOutcome(
            plan=base_plan,
            success_probability=success_prob,
            expected_duration=avg_duration,
            risk_score=risk_score,
            failure_points=failure_points,
            alternate_paths=alternate_paths
        )
    
    def _simulate_futures(
        self,
        plan: list[Action],
        state: WorldState,
        num_futures: int,
        depth: int
    ) -> list[dict[str, Any]]:
        """Simulate plan execution across multiple possible futures"""
        
        # For performance, batch simulations
        batch_size = min(100, num_futures)
        num_batches = (num_futures + batch_size - 1) // batch_size
        
        all_outcomes = []
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures_list = []
            
            for _ in range(num_batches):
                future = executor.submit(
                    self._simulate_batch,
                    plan,
                    state,
                    batch_size,
                    depth
                )
                futures_list.append(future)
            
            for future in as_completed(futures_list):
                all_outcomes.extend(future.result())
        
        return all_outcomes[:num_futures]
    
    @staticmethod
    def _simulate_batch(
        plan: list[Action],
        state: WorldState,
        batch_size: int,
        depth: int
    ) -> list[dict[str, Any]]:
        """Simulate a batch of futures (static method for multiprocessing)"""
        outcomes = []
        
        for _ in range(batch_size):
            outcome = QuantumPlanner._simulate_single_future(plan, state, depth)
            outcomes.append(outcome)
        
        return outcomes
    
    @staticmethod
    def _simulate_single_future(
        plan: list[Action],
        state: WorldState,
        depth: int
    ) -> dict[str, Any]:
        """Simulate single future execution"""
        success = True
        duration = 0.0
        failed_at = -1
        
        for i, action in enumerate(plan[:depth]):
            # Simulate action execution with random failure
            action_success_prob = QuantumPlanner._estimate_action_success(action, state)
            
            if random.random() > action_success_prob:
                success = False
                failed_at = i
                break
            
            # Simulate duration
            duration += random.uniform(1.0, 5.0)
        
        return {
            'success': success,
            'duration': duration,
            'failed_at': failed_at
        }
    
    @staticmethod
    def _estimate_action_success(action: Action, state: WorldState) -> float:
        """Estimate probability of action success"""
        # Base success rate
        base_rate = 0.95
        
        # Adjust based on action type
        risky_actions = ['grasp', 'navigate_to', 'open_door']
        if action.action_type in risky_actions:
            base_rate = 0.85
        
        # Adjust based on state (battery, obstacles, etc.)
        if hasattr(state, 'battery_level') and state.battery_level < 20:
            base_rate *= 0.9
        
        return base_rate
    
    def _calculate_risk(self, outcomes: list[dict[str, Any]]) -> float:
        """Calculate overall risk score (0=safe, 1=risky)"""
        failure_rate = sum(1 for o in outcomes if not o['success']) / len(outcomes)
        
        # Consider variance in duration
        durations = [o['duration'] for o in outcomes]
        avg_duration = sum(durations) / len(durations)
        variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)
        duration_risk = min(variance / 100.0, 0.5)  # Normalize
        
        return failure_rate * 0.7 + duration_risk * 0.3
    
    def _identify_failure_points(self, outcomes: list[dict[str, Any]]) -> list[int]:
        """Identify action indices where failures commonly occur"""
        failure_counts: dict[int, int] = {}
        
        for outcome in outcomes:
            if not outcome['success'] and outcome['failed_at'] >= 0:
                idx = outcome['failed_at']
                failure_counts[idx] = failure_counts.get(idx, 0) + 1
        
        # Return indices with >10% failure rate
        threshold = len(outcomes) * 0.1
        return [idx for idx, count in failure_counts.items() if count >= threshold]
    
    def _generate_alternates(
        self,
        plan: list[Action],
        failure_points: list[int],
        state: WorldState
    ) -> list[list[Action]]:
        """Generate alternate action sequences for failure points"""
        alternates = []
        
        for idx in failure_points:
            if idx >= len(plan):
                continue
            
            failed_action = plan[idx]
            
            # Generate alternate actions
            alt_actions = self._generate_alternate_actions(failed_action, state)
            
            # Create alternate plan
            alt_plan = plan[:idx] + alt_actions + plan[idx+1:]
            alternates.append(alt_plan)
        
        return alternates
    
    def _generate_alternate_actions(self, action: Action, state: WorldState) -> list[Action]:
        """Generate alternate actions for a risky action"""
        alternates = []
        
        if action.action_type == 'navigate_to':
            # Add obstacle check before navigation
            alternates.append(Action('check_path', location=action.location))
            alternates.append(action)
        
        elif action.action_type == 'grasp':
            # Add verification before grasp
            alternates.append(Action('verify_object', target=action.target))
            alternates.append(action)
        
        elif action.action_type == 'open_door':
            # Check if door is locked first
            alternates.append(Action('check_door_state', location=action.location))
            alternates.append(action)
        
        else:
            alternates.append(action)
        
        return alternates
    
    def get_best_plan(self, outcome: PlanOutcome) -> list[Action]:
        """Get best plan considering success probability and risk"""
        if outcome.success_probability > 0.8 and outcome.risk_score < 0.3:
            return outcome.plan
        
        # If base plan is risky, try alternates
        if outcome.alternate_paths:
            # Return first alternate (could be improved with more simulation)
            return outcome.alternate_paths[0]
        
        return outcome.plan
