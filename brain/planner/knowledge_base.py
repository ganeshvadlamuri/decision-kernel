"""Knowledge base for learning from failures and storing behavioral patterns"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import json


@dataclass
class FailurePattern:
    """Pattern of recurring failures"""
    action_type: str
    failure_reason: str
    context: dict
    occurrences: int = 1
    last_seen: datetime = field(default_factory=datetime.now)
    successful_recovery: str | None = None
    recovery_success_rate: float = 0.0


@dataclass
class LearnedBehavior:
    """Successful behavior pattern learned from experience"""
    goal_type: str
    context_conditions: dict
    action_sequence: list[str]
    success_count: int = 0
    failure_count: int = 0
    avg_execution_time: float = 0.0
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0


class KnowledgeBase:
    """Store and retrieve learned behaviors and failure patterns"""
    
    def __init__(self, persistence_path: str | None = None):
        self.failure_patterns: Dict[str, FailurePattern] = {}
        self.learned_behaviors: List[LearnedBehavior] = []
        self.context_preferences: Dict[str, dict] = {}
        self.persistence_path = persistence_path
        
        if persistence_path:
            self.load()
    
    def record_failure(
        self,
        action_type: str,
        failure_reason: str,
        context: dict,
        recovery_strategy: str | None = None,
        recovery_successful: bool = False
    ):
        """Record a failure occurrence"""
        key = f"{action_type}:{failure_reason}"
        
        if key in self.failure_patterns:
            pattern = self.failure_patterns[key]
            pattern.occurrences += 1
            pattern.last_seen = datetime.now()
            
            if recovery_successful and recovery_strategy:
                pattern.successful_recovery = recovery_strategy
                # Update success rate
                old_rate = pattern.recovery_success_rate
                pattern.recovery_success_rate = (old_rate * (pattern.occurrences - 1) + 1.0) / pattern.occurrences
        else:
            self.failure_patterns[key] = FailurePattern(
                action_type=action_type,
                failure_reason=failure_reason,
                context=context,
                successful_recovery=recovery_strategy if recovery_successful else None,
                recovery_success_rate=1.0 if recovery_successful else 0.0
            )
    
    def get_best_recovery(self, action_type: str, failure_reason: str) -> str | None:
        """Get most successful recovery strategy for a failure"""
        key = f"{action_type}:{failure_reason}"
        
        if key in self.failure_patterns:
            pattern = self.failure_patterns[key]
            if pattern.recovery_success_rate > 0.5:  # >50% success rate
                return pattern.successful_recovery
        
        return None
    
    def record_behavior(
        self,
        goal_type: str,
        context: dict,
        actions: list[str],
        success: bool,
        execution_time: float
    ):
        """Record execution of a behavior"""
        # Find matching learned behavior
        matching = None
        for behavior in self.learned_behaviors:
            if behavior.goal_type == goal_type and self._context_matches(behavior.context_conditions, context):
                matching = behavior
                break
        
        if matching:
            if success:
                matching.success_count += 1
            else:
                matching.failure_count += 1
            
            # Update average execution time
            total_executions = matching.success_count + matching.failure_count
            matching.avg_execution_time = (
                (matching.avg_execution_time * (total_executions - 1) + execution_time) / total_executions
            )
        else:
            # Create new learned behavior
            self.learned_behaviors.append(LearnedBehavior(
                goal_type=goal_type,
                context_conditions=context,
                action_sequence=actions,
                success_count=1 if success else 0,
                failure_count=0 if success else 1,
                avg_execution_time=execution_time
            ))
    
    def get_best_behavior(self, goal_type: str, context: dict) -> LearnedBehavior | None:
        """Get most successful behavior for goal in given context"""
        candidates = [
            b for b in self.learned_behaviors
            if b.goal_type == goal_type and self._context_matches(b.context_conditions, context)
        ]
        
        if not candidates:
            return None
        
        # Sort by success rate, then by execution count
        candidates.sort(
            key=lambda b: (b.success_rate, b.success_count + b.failure_count),
            reverse=True
        )
        
        return candidates[0] if candidates[0].success_rate > 0.3 else None
    
    def update_context_preference(self, context_key: str, preference: dict):
        """Store context-specific preferences (time of day, battery level, etc.)"""
        self.context_preferences[context_key] = preference
    
    def get_context_preference(self, context_key: str) -> dict | None:
        """Retrieve context-specific preference"""
        return self.context_preferences.get(context_key)
    
    def get_failure_statistics(self) -> dict:
        """Get statistics about failures"""
        stats = {
            'total_patterns': len(self.failure_patterns),
            'most_common': [],
            'best_recoveries': []
        }
        
        # Most common failures
        sorted_patterns = sorted(
            self.failure_patterns.values(),
            key=lambda p: p.occurrences,
            reverse=True
        )
        stats['most_common'] = [
            {
                'action': p.action_type,
                'reason': p.failure_reason,
                'count': p.occurrences
            }
            for p in sorted_patterns[:5]
        ]
        
        # Best recovery strategies
        recoverable = [p for p in self.failure_patterns.values() if p.successful_recovery]
        recoverable.sort(key=lambda p: p.recovery_success_rate, reverse=True)
        stats['best_recoveries'] = [
            {
                'action': p.action_type,
                'reason': p.failure_reason,
                'recovery': p.successful_recovery,
                'success_rate': p.recovery_success_rate
            }
            for p in recoverable[:5]
        ]
        
        return stats
    
    def get_behavior_statistics(self) -> dict:
        """Get statistics about learned behaviors"""
        return {
            'total_behaviors': len(self.learned_behaviors),
            'best_performers': [
                {
                    'goal': b.goal_type,
                    'success_rate': b.success_rate,
                    'executions': b.success_count + b.failure_count,
                    'avg_time': b.avg_execution_time
                }
                for b in sorted(self.learned_behaviors, key=lambda b: b.success_rate, reverse=True)[:5]
            ]
        }
    
    def _context_matches(self, stored_context: dict, current_context: dict) -> bool:
        """Check if contexts match (fuzzy matching)"""
        if not stored_context:
            return True
        
        matches = 0
        for key, value in stored_context.items():
            if key in current_context and current_context[key] == value:
                matches += 1
        
        # At least 70% of stored context must match
        return matches / len(stored_context) >= 0.7 if stored_context else True
    
    def save(self):
        """Persist knowledge base to disk"""
        if not self.persistence_path:
            return
        
        data = {
            'failure_patterns': {
                k: {
                    'action_type': v.action_type,
                    'failure_reason': v.failure_reason,
                    'context': v.context,
                    'occurrences': v.occurrences,
                    'last_seen': v.last_seen.isoformat(),
                    'successful_recovery': v.successful_recovery,
                    'recovery_success_rate': v.recovery_success_rate
                }
                for k, v in self.failure_patterns.items()
            },
            'learned_behaviors': [
                {
                    'goal_type': b.goal_type,
                    'context_conditions': b.context_conditions,
                    'action_sequence': b.action_sequence,
                    'success_count': b.success_count,
                    'failure_count': b.failure_count,
                    'avg_execution_time': b.avg_execution_time
                }
                for b in self.learned_behaviors
            ],
            'context_preferences': self.context_preferences
        }
        
        with open(self.persistence_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load knowledge base from disk"""
        if not self.persistence_path:
            return
        
        try:
            with open(self.persistence_path, 'r') as f:
                data = json.load(f)
            
            # Load failure patterns
            for k, v in data.get('failure_patterns', {}).items():
                self.failure_patterns[k] = FailurePattern(
                    action_type=v['action_type'],
                    failure_reason=v['failure_reason'],
                    context=v['context'],
                    occurrences=v['occurrences'],
                    last_seen=datetime.fromisoformat(v['last_seen']),
                    successful_recovery=v.get('successful_recovery'),
                    recovery_success_rate=v.get('recovery_success_rate', 0.0)
                )
            
            # Load learned behaviors
            for b in data.get('learned_behaviors', []):
                self.learned_behaviors.append(LearnedBehavior(
                    goal_type=b['goal_type'],
                    context_conditions=b['context_conditions'],
                    action_sequence=b['action_sequence'],
                    success_count=b['success_count'],
                    failure_count=b['failure_count'],
                    avg_execution_time=b['avg_execution_time']
                ))
            
            # Load context preferences
            self.context_preferences = data.get('context_preferences', {})
            
        except FileNotFoundError:
            pass  # Fresh start
