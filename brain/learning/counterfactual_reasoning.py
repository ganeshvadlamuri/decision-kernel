"""Counterfactual Reasoning - Learn from paths not taken."""
from dataclasses import dataclass
from typing import List, Dict, Any
from brain.planner.actions import Action


@dataclass
class CounterfactualOutcome:
    action_taken: Action
    actual_outcome: str
    alternate_actions: List[Action]
    alternate_outcomes: List[str]
    regret_score: float
    learning: str


class CounterfactualReasoning:
    def __init__(self):
        self.counterfactual_history: List[CounterfactualOutcome] = []
        self.learned_preferences: Dict[str, float] = {}
    
    def simulate_counterfactuals(self, action_taken: Action, actual_outcome: str,
                                 context: Dict[str, Any]) -> CounterfactualOutcome:
        """Simulate what would have happened with different actions."""
        # Generate alternate actions
        alternates = self._generate_alternates(action_taken, context)
        
        # Simulate outcomes for each alternate
        alternate_outcomes = []
        for alt_action in alternates:
            outcome = self._simulate_outcome(alt_action, context)
            alternate_outcomes.append(outcome)
        
        # Calculate regret (how much better could we have done?)
        actual_score = self._score_outcome(actual_outcome)
        best_alternate_score = max([self._score_outcome(o) for o in alternate_outcomes], default=0.0)
        regret_score = max(0.0, best_alternate_score - actual_score)
        
        # Generate learning
        learning = self._extract_learning(action_taken, actual_outcome, alternates, alternate_outcomes, regret_score)
        
        counterfactual = CounterfactualOutcome(
            action_taken=action_taken,
            actual_outcome=actual_outcome,
            alternate_actions=alternates,
            alternate_outcomes=alternate_outcomes,
            regret_score=regret_score,
            learning=learning
        )
        
        self.counterfactual_history.append(counterfactual)
        return counterfactual
    
    def _generate_alternates(self, action: Action, context: Dict[str, Any]) -> List[Action]:
        """Generate plausible alternate actions."""
        alternates = []
        
        if action.action_type == "navigate":
            alternates.append(Action(action_type="wait", parameters={"duration": 5}))
            alternates.append(Action(action_type="navigate", location="alternate_route", parameters={"speed": "fast"}))
        elif action.action_type == "grasp":
            alternates.append(Action(action_type="grasp", target=action.target, parameters={"grip": "soft"}))
            alternates.append(Action(action_type="scan", target=action.target, parameters={}))
        elif action.action_type == "wait":
            alternates.append(Action(action_type="navigate", location="storage", parameters={}))
        
        return alternates[:3]
    
    def _simulate_outcome(self, action: Action, context: Dict[str, Any]) -> str:
        """Simulate outcome of an action."""
        if action.action_type == "wait":
            return "delayed_completion"
        elif action.action_type == "navigate" and action.parameters.get("speed") == "fast":
            return "faster_completion"
        elif action.action_type == "grasp" and action.parameters.get("grip") == "soft":
            return "safer_handling"
        elif action.action_type == "scan":
            return "better_accuracy"
        return "similar_outcome"
    
    def _score_outcome(self, outcome: str) -> float:
        """Score an outcome (higher is better)."""
        scores = {
            "success": 10.0,
            "faster_completion": 9.0,
            "safer_handling": 8.5,
            "better_accuracy": 8.0,
            "similar_outcome": 7.0,
            "delayed_completion": 5.0,
            "failure": 0.0
        }
        return scores.get(outcome, 5.0)
    
    def _extract_learning(self, action: Action, actual: str, alternates: List[Action],
                         alt_outcomes: List[str], regret: float) -> str:
        """Extract learning from counterfactual analysis."""
        if regret > 3.0:
            best_idx = max(range(len(alt_outcomes)), key=lambda i: self._score_outcome(alt_outcomes[i]))
            best_action = alternates[best_idx]
            return f"Should have used {best_action.action_type} instead of {action.action_type}"
        elif regret > 1.0:
            return f"Could slightly improve by adjusting parameters"
        else:
            return f"Action {action.action_type} was optimal"
    
    def learn_from_paths_not_taken(self) -> Dict[str, Any]:
        """Analyze all counterfactuals and extract patterns."""
        if not self.counterfactual_history:
            return {"status": "no_data"}
        
        total_regret = sum(cf.regret_score for cf in self.counterfactual_history)
        avg_regret = total_regret / len(self.counterfactual_history)
        
        # Find patterns
        high_regret_actions = [cf.action_taken.action_type for cf in self.counterfactual_history if cf.regret_score > 2.0]
        
        return {
            "total_counterfactuals": len(self.counterfactual_history),
            "avg_regret": avg_regret,
            "high_regret_actions": list(set(high_regret_actions)),
            "key_learning": "Prefer faster routes and softer grips" if avg_regret > 1.5 else "Current strategy is near-optimal"
        }
    
    def get_best_action_from_history(self, context: Dict[str, Any]) -> str:
        """Recommend best action based on counterfactual learning."""
        if not self.counterfactual_history:
            return "insufficient_data"
        
        # Find similar contexts and their best alternates
        for cf in reversed(self.counterfactual_history[-10:]):
            if cf.regret_score > 2.0 and cf.alternate_outcomes:
                best_idx = max(range(len(cf.alternate_outcomes)), 
                             key=lambda i: self._score_outcome(cf.alternate_outcomes[i]))
                return cf.alternate_actions[best_idx].action_type
        
        return "continue_current_strategy"
