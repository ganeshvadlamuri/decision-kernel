"""Tests for advanced learning capabilities"""
import pytest
from brain.learning.self_evolving_planner import (
    SelfEvolvingPlanner,
    ObservedAction,
    TaskPattern
)
from brain.learning.emotional_intelligence import (
    EmotionalIntelligence,
    Emotion,
    BehaviorMode,
    EmotionalContext
)
from brain.planner.actions import Action
from brain.world.state import WorldState


class TestSelfEvolvingPlanner:
    """Test self-evolving task learning"""
    
    def test_learns_task_from_observations(self):
        """Test: Learns task after minimum observations"""
        planner = SelfEvolvingPlanner(min_observations=3, confidence_threshold=0.7)
        
        # Observe making sandwich 3 times
        for _ in range(3):
            actions = [
                ObservedAction('navigate_to', None, 'kitchen', 0.0, {}),
                ObservedAction('grasp', 'bread', None, 1.0, {}),
                ObservedAction('grasp', 'cheese', None, 2.0, {}),
                ObservedAction('assemble', 'sandwich', None, 3.0, {})
            ]
            planner.observe_demonstration('make_sandwich', actions)
        
        # Should have learned the task
        learned = planner.get_learned_task('make_sandwich')
        assert learned is not None
        assert learned.observation_count == 3
        assert learned.confidence >= 0.7
    
    def test_requires_minimum_observations(self):
        """Test: Doesn't learn with too few observations"""
        planner = SelfEvolvingPlanner(min_observations=5)
        
        # Only 2 observations
        for _ in range(2):
            actions = [ObservedAction('grasp', 'cup', None, 0.0, {})]
            planner.observe_demonstration('test_task', actions)
        
        learned = planner.get_learned_task('test_task')
        assert learned is None
    
    def test_generates_decomposition_code(self):
        """Test: Generates Python code for learned task"""
        planner = SelfEvolvingPlanner(min_observations=2, confidence_threshold=0.5)
        
        for _ in range(2):
            actions = [
                ObservedAction('navigate_to', None, 'kitchen', 0.0, {}),
                ObservedAction('grasp', 'cup', None, 1.0, {})
            ]
            planner.observe_demonstration('get_cup', actions)
        
        code = planner.generate_decomposition_code('get_cup')
        assert 'def _decompose_get_cup' in code
        assert 'navigate_to' in code
        assert 'grasp' in code


class TestEmotionalIntelligence:
    """Test emotional intelligence adaptation"""
    
    def test_detects_emotion_from_state(self):
        """Test: Detects human emotion from world state"""
        ei = EmotionalIntelligence()
        state = WorldState()
        state.human_emotion = 'stressed'
        state.emotion_intensity = 0.8
        
        context = ei.detect_emotion(state)
        assert context.primary_emotion == Emotion.STRESSED
        assert context.intensity == 0.8
    
    def test_adapts_plan_for_stressed_human(self):
        """Test: Adapts plan when human is stressed"""
        ei = EmotionalIntelligence()
        
        plan = [
            Action('navigate_to', location='kitchen'),
            Action('grasp', target='cup')
        ]
        
        context = EmotionalContext(
            primary_emotion=Emotion.STRESSED,
            intensity=0.9,
            duration=0.0,
            triggers=[],
            preferences={}
        )
        
        adapted = ei.adapt_plan(plan, context, WorldState())
        
        # Should use gentle or minimal mode
        assert adapted.behavior_mode in [BehaviorMode.GENTLE, BehaviorMode.MINIMAL]
        # Should add pauses
        assert len(adapted.adapted_plan) > len(plan)
        # Should have modifications
        assert len(adapted.modifications) > 0
    
    def test_adapts_plan_for_happy_human(self):
        """Test: Uses efficient mode when human is happy"""
        ei = EmotionalIntelligence()
        
        plan = [Action('navigate_to', location='kitchen')]
        
        context = EmotionalContext(
            primary_emotion=Emotion.HAPPY,
            intensity=0.7,
            duration=0.0,
            triggers=[],
            preferences={}
        )
        
        adapted = ei.adapt_plan(plan, context, WorldState())
        assert adapted.behavior_mode == BehaviorMode.EFFICIENT
    
    def test_should_interrupt_for_high_stress(self):
        """Test: Recommends interrupting plan for high stress"""
        ei = EmotionalIntelligence()
        
        context = EmotionalContext(
            primary_emotion=Emotion.STRESSED,
            intensity=0.9,
            duration=0.0,
            triggers=[],
            preferences={}
        )
        
        assert ei.should_interrupt_plan(context)
    
    def test_generates_comfort_action(self):
        """Test: Generates appropriate comfort action"""
        ei = EmotionalIntelligence()
        
        action = ei.generate_comfort_action(Emotion.SAD)
        assert action.action_type == 'offer_assistance'
        
        action = ei.generate_comfort_action(Emotion.ANGRY)
        assert action.action_type == 'give_space'
    
    def test_comfort_score_calculation(self):
        """Test: Calculates comfort score"""
        ei = EmotionalIntelligence()
        
        plan = [Action('navigate_to', location='kitchen')]
        context = EmotionalContext(
            primary_emotion=Emotion.CALM,
            intensity=0.5,
            duration=0.0,
            triggers=[],
            preferences={}
        )
        
        adapted = ei.adapt_plan(plan, context, WorldState())
        assert 0.0 <= adapted.estimated_comfort_score <= 1.0
