"""Emotional Intelligence Layer - Adapt behavior based on human emotions"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from brain.planner.actions import Action
from brain.world.state import WorldState


class Emotion(Enum):
    """Human emotional states"""
    HAPPY = "happy"
    SAD = "sad"
    STRESSED = "stressed"
    ANGRY = "angry"
    CALM = "calm"
    EXCITED = "excited"
    TIRED = "tired"
    ANXIOUS = "anxious"


class BehaviorMode(Enum):
    """Robot behavior modes"""
    GENTLE = "gentle"          # Slow, quiet, careful
    EFFICIENT = "efficient"    # Fast, direct
    SUPPORTIVE = "supportive"  # Comforting, helpful
    MINIMAL = "minimal"        # Stay out of way
    ENERGETIC = "energetic"    # Match human energy
    CAUTIOUS = "cautious"      # Extra careful


@dataclass
class EmotionalContext:
    """Context about human emotional state"""
    primary_emotion: Emotion
    intensity: float  # 0.0 to 1.0
    duration: float   # seconds
    triggers: list[str]
    preferences: dict[str, Any]


@dataclass
class AdaptedPlan:
    """Plan adapted to emotional context"""
    original_plan: list[Action]
    adapted_plan: list[Action]
    behavior_mode: BehaviorMode
    modifications: list[str]
    estimated_comfort_score: float


class EmotionalIntelligence:
    """Adapts robot behavior based on human emotional state"""

    def __init__(self):
        self.emotion_to_mode = {
            Emotion.HAPPY: BehaviorMode.EFFICIENT,
            Emotion.SAD: BehaviorMode.SUPPORTIVE,
            Emotion.STRESSED: BehaviorMode.GENTLE,
            Emotion.ANGRY: BehaviorMode.MINIMAL,
            Emotion.CALM: BehaviorMode.EFFICIENT,
            Emotion.EXCITED: BehaviorMode.ENERGETIC,
            Emotion.TIRED: BehaviorMode.GENTLE,
            Emotion.ANXIOUS: BehaviorMode.CAUTIOUS
        }

        self.mode_parameters: dict[BehaviorMode, dict[str, Any]] = {
            BehaviorMode.GENTLE: {
                'speed_multiplier': 0.5,
                'noise_reduction': 0.8,
                'approach_distance': 2.0,
                'pause_duration': 2.0
            },
            BehaviorMode.EFFICIENT: {
                'speed_multiplier': 1.0,
                'noise_reduction': 0.0,
                'approach_distance': 1.0,
                'pause_duration': 0.5
            },
            BehaviorMode.SUPPORTIVE: {
                'speed_multiplier': 0.7,
                'noise_reduction': 0.5,
                'approach_distance': 1.5,
                'pause_duration': 1.5,
                'check_in_frequency': 'high'
            },
            BehaviorMode.MINIMAL: {
                'speed_multiplier': 0.6,
                'noise_reduction': 0.9,
                'approach_distance': 3.0,
                'pause_duration': 3.0,
                'avoid_interaction': True
            },
            BehaviorMode.ENERGETIC: {
                'speed_multiplier': 1.2,
                'noise_reduction': 0.0,
                'approach_distance': 0.8,
                'pause_duration': 0.2
            },
            BehaviorMode.CAUTIOUS: {
                'speed_multiplier': 0.4,
                'noise_reduction': 0.7,
                'approach_distance': 2.5,
                'pause_duration': 2.5,
                'verification_steps': True
            }
        }

    def detect_emotion(self, state: WorldState) -> EmotionalContext:
        """Detect human emotion from world state"""
        # In real implementation, this would use:
        # - Facial expression recognition
        # - Voice tone analysis
        # - Body language
        # - Context (time of day, recent events)

        # Simulated detection from state
        emotion = Emotion.CALM
        intensity = 0.5

        if hasattr(state, 'human_emotion'):
            emotion = Emotion(state.human_emotion)

        if hasattr(state, 'emotion_intensity'):
            intensity = state.emotion_intensity

        # Infer from context
        if hasattr(state, 'time_of_day'):
            if state.time_of_day == 'night' and hasattr(state, 'noise_level'):
                if state.noise_level > 50:
                    emotion = Emotion.STRESSED
                    intensity = 0.7

        return EmotionalContext(
            primary_emotion=emotion,
            intensity=intensity,
            duration=0.0,
            triggers=[],
            preferences={}
        )

    def adapt_plan(
        self,
        plan: list[Action],
        emotional_context: EmotionalContext,
        state: WorldState
    ) -> AdaptedPlan:
        """Adapt plan based on emotional context"""

        # Determine behavior mode
        mode = self.emotion_to_mode.get(
            emotional_context.primary_emotion,
            BehaviorMode.EFFICIENT
        )

        # Adjust mode based on intensity
        if emotional_context.intensity > 0.8:
            if mode == BehaviorMode.GENTLE:
                mode = BehaviorMode.MINIMAL  # Give more space
            elif mode == BehaviorMode.EFFICIENT:
                mode = BehaviorMode.CAUTIOUS  # Be more careful

        # Apply adaptations
        adapted_plan = self._apply_mode(plan, mode, state)
        modifications = self._get_modifications(plan, adapted_plan, mode)
        comfort_score = self._estimate_comfort(adapted_plan, emotional_context, mode)

        return AdaptedPlan(
            original_plan=plan,
            adapted_plan=adapted_plan,
            behavior_mode=mode,
            modifications=modifications,
            estimated_comfort_score=comfort_score
        )

    def _apply_mode(
        self,
        plan: list[Action],
        mode: BehaviorMode,
        state: WorldState
    ) -> list[Action]:
        """Apply behavior mode to plan"""
        params = self.mode_parameters[mode]
        adapted = []

        for action in plan:
            # Modify action based on mode
            modified_action = Action(
                action_type=action.action_type,
                target=action.target,
                location=action.location,
                parameters={**action.parameters}
            )

            # Add mode-specific parameters
            modified_action.parameters['speed_multiplier'] = params['speed_multiplier']
            modified_action.parameters['noise_reduction'] = params['noise_reduction']

            # Add pauses for gentle/supportive modes
            if mode in [BehaviorMode.GENTLE, BehaviorMode.SUPPORTIVE, BehaviorMode.MINIMAL]:
                if action.action_type in ['navigate_to', 'grasp', 'release']:
                    # Add pause before action
                    adapted.append(Action(
                        'pause',
                        parameters={'duration': params['pause_duration']}
                    ))

            # Add verification for cautious mode
            if mode == BehaviorMode.CAUTIOUS and params.get('verification_steps'):
                if action.action_type == 'grasp':
                    adapted.append(Action('verify_safe_to_grasp', target=action.target))
                elif action.action_type == 'navigate_to':
                    adapted.append(Action('scan_path', location=action.location))

            # Add check-ins for supportive mode
            if mode == BehaviorMode.SUPPORTIVE and params.get('check_in_frequency') == 'high':
                if action.action_type in ['navigate_to', 'release']:
                    adapted.append(Action('check_human_comfort', parameters={}))

            # Avoid interaction for minimal mode
            if mode == BehaviorMode.MINIMAL and params.get('avoid_interaction'):
                if action.action_type in ['alert_human', 'wait_for_human']:
                    # Skip interactive actions
                    continue

            adapted.append(modified_action)

        return adapted

    def _get_modifications(
        self,
        original: list[Action],
        adapted: list[Action],
        mode: BehaviorMode
    ) -> list[str]:
        """List modifications made to plan"""
        mods = []

        if len(adapted) > len(original):
            mods.append(f"Added {len(adapted) - len(original)} safety/comfort actions")

        mods.append(f"Applied {mode.value} behavior mode")

        params = self.mode_parameters[mode]
        if params['speed_multiplier'] < 1.0:
            mods.append(f"Reduced speed to {params['speed_multiplier']*100:.0f}%")

        if params['noise_reduction'] > 0:
            mods.append(f"Reduced noise by {params['noise_reduction']*100:.0f}%")

        return mods

    def _estimate_comfort(
        self,
        plan: list[Action],
        context: EmotionalContext,
        mode: BehaviorMode
    ) -> float:
        """Estimate human comfort score with adapted plan"""
        base_score = 0.5

        # Mode appropriateness
        if mode == self.emotion_to_mode.get(context.primary_emotion):
            base_score += 0.3

        # Intensity consideration
        if context.intensity > 0.7:
            # High intensity emotions need more adaptation
            if mode in [BehaviorMode.GENTLE, BehaviorMode.MINIMAL, BehaviorMode.SUPPORTIVE]:
                base_score += 0.2

        # Plan length (shorter is better for negative emotions)
        if context.primary_emotion in [Emotion.STRESSED, Emotion.ANGRY, Emotion.ANXIOUS]:
            if len(plan) < 10:
                base_score += 0.1

        return min(base_score, 1.0)

    def should_interrupt_plan(self, emotional_context: EmotionalContext) -> bool:
        """Determine if current plan should be interrupted due to emotion change"""
        # Interrupt for high-intensity negative emotions
        negative_emotions = [Emotion.ANGRY, Emotion.STRESSED, Emotion.ANXIOUS]

        if emotional_context.primary_emotion in negative_emotions:
            if emotional_context.intensity > 0.8:
                return True

        return False

    def generate_comfort_action(self, emotion: Emotion) -> Action:
        """Generate action to comfort human based on emotion"""
        comfort_actions = {
            Emotion.SAD: Action('offer_assistance', parameters={'message': 'Can I help with anything?'}),
            Emotion.STRESSED: Action('reduce_activity', parameters={'mode': 'quiet'}),
            Emotion.ANGRY: Action('give_space', parameters={'distance': 5.0}),
            Emotion.ANXIOUS: Action('provide_reassurance', parameters={'message': 'Everything is under control'}),
            Emotion.TIRED: Action('dim_lights', parameters={'level': 0.3})
        }

        return comfort_actions.get(emotion, Action('continue_normal', parameters={}))
