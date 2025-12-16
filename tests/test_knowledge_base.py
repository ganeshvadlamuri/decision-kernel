"""Tests for knowledge base learning system"""
import pytest
from brain.planner.knowledge_base import KnowledgeBase, FailurePattern, LearnedBehavior


class TestKnowledgeBase:
    """Test learning from failures and behaviors"""
    
    def setup_method(self):
        self.kb = KnowledgeBase()
    
    def test_record_failure_creates_pattern(self):
        """Test: Recording failure creates pattern"""
        self.kb.record_failure('navigate_to', 'path_blocked', {'location': 'kitchen'})
        
        assert len(self.kb.failure_patterns) == 1
        pattern = list(self.kb.failure_patterns.values())[0]
        assert pattern.action_type == 'navigate_to'
        assert pattern.failure_reason == 'path_blocked'
        assert pattern.occurrences == 1
    
    def test_record_failure_increments_occurrences(self):
        """Test: Recording same failure increments count"""
        self.kb.record_failure('navigate_to', 'path_blocked', {'location': 'kitchen'})
        self.kb.record_failure('navigate_to', 'path_blocked', {'location': 'bedroom'})
        
        assert len(self.kb.failure_patterns) == 1
        pattern = list(self.kb.failure_patterns.values())[0]
        assert pattern.occurrences == 2
    
    def test_record_successful_recovery(self):
        """Test: Records successful recovery strategy"""
        self.kb.record_failure(
            'navigate_to', 'path_blocked', {'location': 'kitchen'},
            recovery_strategy='find_alternative_route',
            recovery_successful=True
        )
        
        pattern = list(self.kb.failure_patterns.values())[0]
        assert pattern.successful_recovery == 'find_alternative_route'
        assert pattern.recovery_success_rate == 1.0
    
    def test_get_best_recovery(self):
        """Test: Retrieves best recovery strategy"""
        self.kb.record_failure(
            'grasp', 'object_not_found', {},
            recovery_strategy='search_area',
            recovery_successful=True
        )
        
        recovery = self.kb.get_best_recovery('grasp', 'object_not_found')
        assert recovery == 'search_area'
    
    def test_get_best_recovery_requires_threshold(self):
        """Test: Only returns recovery with >50% success rate"""
        # Record failure with low success rate
        self.kb.record_failure('grasp', 'slippery', {}, recovery_strategy='retry', recovery_successful=False)
        
        recovery = self.kb.get_best_recovery('grasp', 'slippery')
        assert recovery is None
    
    def test_record_behavior_creates_learned_behavior(self):
        """Test: Recording behavior creates learned behavior"""
        self.kb.record_behavior(
            'bring', {'battery': 80}, ['navigate', 'grasp', 'release'],
            success=True, execution_time=10.5
        )
        
        assert len(self.kb.learned_behaviors) == 1
        behavior = self.kb.learned_behaviors[0]
        assert behavior.goal_type == 'bring'
        assert behavior.success_count == 1
        assert behavior.avg_execution_time == 10.5
    
    def test_record_behavior_updates_existing(self):
        """Test: Recording same behavior updates statistics"""
        context = {'battery': 80}
        self.kb.record_behavior('bring', context, ['nav', 'grasp'], True, 10.0)
        self.kb.record_behavior('bring', context, ['nav', 'grasp'], True, 12.0)
        
        assert len(self.kb.learned_behaviors) == 1
        behavior = self.kb.learned_behaviors[0]
        assert behavior.success_count == 2
        assert behavior.avg_execution_time == 11.0
    
    def test_get_best_behavior(self):
        """Test: Retrieves best behavior for goal"""
        context = {'battery': 80, 'time': 'day'}
        self.kb.record_behavior('bring', context, ['nav', 'grasp'], True, 10.0)
        self.kb.record_behavior('bring', context, ['nav', 'grasp'], True, 11.0)
        
        best = self.kb.get_best_behavior('bring', context)
        assert best is not None
        assert best.goal_type == 'bring'
        assert best.success_rate == 1.0
    
    def test_get_best_behavior_requires_threshold(self):
        """Test: Only returns behavior with >30% success rate"""
        context = {'battery': 80}
        self.kb.record_behavior('bring', context, ['nav'], False, 10.0)
        self.kb.record_behavior('bring', context, ['nav'], False, 11.0)
        self.kb.record_behavior('bring', context, ['nav'], False, 12.0)
        self.kb.record_behavior('bring', context, ['nav'], True, 13.0)
        
        best = self.kb.get_best_behavior('bring', context)
        assert best is None  # 25% success rate < 30% threshold
    
    def test_context_matching_fuzzy(self):
        """Test: Context matching is fuzzy (70% threshold)"""
        stored_context = {'battery': 80, 'time': 'day', 'location': 'home'}
        self.kb.record_behavior('bring', stored_context, ['nav'], True, 10.0)
        
        # 2 out of 3 match = 66% < 70%
        query_context = {'battery': 80, 'time': 'day', 'location': 'office'}
        best = self.kb.get_best_behavior('bring', query_context)
        assert best is None
        
        # 3 out of 3 match = 100% >= 70%
        query_context2 = {'battery': 80, 'time': 'day', 'location': 'home'}
        best2 = self.kb.get_best_behavior('bring', query_context2)
        assert best2 is not None
    
    def test_failure_statistics(self):
        """Test: Get failure statistics"""
        self.kb.record_failure('navigate_to', 'blocked', {})
        self.kb.record_failure('navigate_to', 'blocked', {})
        self.kb.record_failure('grasp', 'not_found', {})
        
        stats = self.kb.get_failure_statistics()
        assert stats['total_patterns'] == 2
        assert len(stats['most_common']) == 2
        assert stats['most_common'][0]['count'] == 2
    
    def test_behavior_statistics(self):
        """Test: Get behavior statistics"""
        self.kb.record_behavior('bring', {}, ['nav'], True, 10.0)
        self.kb.record_behavior('clean', {}, ['nav'], True, 15.0)
        
        stats = self.kb.get_behavior_statistics()
        assert stats['total_behaviors'] == 2
        assert len(stats['best_performers']) == 2
    
    def test_context_preferences(self):
        """Test: Store and retrieve context preferences"""
        self.kb.update_context_preference('night_mode', {'speed': 'slow', 'lights': 'on'})
        
        pref = self.kb.get_context_preference('night_mode')
        assert pref == {'speed': 'slow', 'lights': 'on'}
    
    def test_learned_behavior_success_rate(self):
        """Test: Success rate calculation"""
        behavior = LearnedBehavior(
            goal_type='test',
            context_conditions={},
            action_sequence=[],
            success_count=7,
            failure_count=3
        )
        
        assert behavior.success_rate == 0.7
