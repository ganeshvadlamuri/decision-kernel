"""Self-Evolving Task Decomposition - Learn tasks by observing humans"""
from collections import defaultdict
from dataclasses import dataclass
import json
from typing import Any


@dataclass
class ObservedAction:
    """Single observed action from human demonstration"""
    action_type: str
    target: str | None
    location: str | None
    timestamp: float
    context: dict[str, Any]


@dataclass
class TaskPattern:
    """Learned pattern from multiple observations"""
    task_name: str
    action_sequence: list[dict]
    preconditions: list[str]
    success_rate: float
    observation_count: int
    confidence: float


class SelfEvolvingPlanner:
    """Learns new task decompositions by observing human demonstrations"""

    def __init__(self, min_observations: int = 5, confidence_threshold: float = 0.8):
        self.observations: dict[str, list[list[ObservedAction]]] = defaultdict(list)
        self.learned_tasks: dict[str, TaskPattern] = {}
        self.min_observations = min_observations
        self.confidence_threshold = confidence_threshold

    def observe_demonstration(self, task_name: str, actions: list[ObservedAction]):
        """Record a human demonstration of a task"""
        self.observations[task_name].append(actions)

        # Auto-learn if enough observations
        if len(self.observations[task_name]) >= self.min_observations:
            self._try_learn_task(task_name)

    def _try_learn_task(self, task_name: str):
        """Attempt to learn task pattern from observations"""
        demos = self.observations[task_name]

        # Find common action sequence
        common_sequence = self._extract_common_sequence(demos)
        if not common_sequence:
            return

        # Extract preconditions
        preconditions = self._extract_preconditions(demos)

        # Calculate confidence
        confidence = self._calculate_confidence(demos, common_sequence)

        if confidence >= self.confidence_threshold:
            self.learned_tasks[task_name] = TaskPattern(
                task_name=task_name,
                action_sequence=common_sequence,
                preconditions=preconditions,
                success_rate=1.0,
                observation_count=len(demos),
                confidence=confidence
            )

    def _extract_common_sequence(self, demos: list[list[ObservedAction]]) -> list[dict]:
        """Find common action sequence across demonstrations"""
        if not demos:
            return []

        # Use longest common subsequence algorithm
        sequences = [[self._action_to_dict(a) for a in demo] for demo in demos]

        # Simple approach: find actions that appear in >80% of demos
        action_frequency: dict[str, int] = defaultdict(int)
        for seq in sequences:
            seen = set()
            for action in seq:
                key = f"{action['action_type']}:{action.get('target', '')}:{action.get('location', '')}"
                if key not in seen:
                    action_frequency[key] += 1
                    seen.add(key)

        threshold = len(demos) * 0.8
        common_actions = [k for k, v in action_frequency.items() if v >= threshold]

        # Reconstruct sequence maintaining order from first demo
        result = []
        for action in sequences[0]:
            key = f"{action['action_type']}:{action.get('target', '')}:{action.get('location', '')}"
            if key in common_actions:
                result.append(action)

        return result

    def _extract_preconditions(self, demos: list[list[ObservedAction]]) -> list[str]:
        """Extract common preconditions from demonstrations"""
        preconditions = []

        # Analyze context of first action in each demo
        first_contexts = [demo[0].context for demo in demos if demo]

        # Find common context keys
        if first_contexts:
            common_keys = set(first_contexts[0].keys())
            for ctx in first_contexts[1:]:
                common_keys &= set(ctx.keys())

            preconditions = [f"check_{key}" for key in common_keys]

        return preconditions

    def _calculate_confidence(self, demos: list[list[ObservedAction]], common_seq: list[dict]) -> float:
        """Calculate confidence in learned pattern"""
        if not demos or not common_seq:
            return 0.0

        # Measure how well common sequence matches each demo
        matches = 0
        for demo in demos:
            demo_actions = [self._action_to_dict(a) for a in demo]
            if self._sequence_matches(demo_actions, common_seq, threshold=0.7):
                matches += 1

        return matches / len(demos)

    def _sequence_matches(self, demo: list[dict], pattern: list[dict], threshold: float) -> bool:
        """Check if demo matches pattern with threshold"""
        if not pattern:
            return False

        matched = sum(1 for p in pattern if any(self._actions_similar(p, d) for d in demo))
        return (matched / len(pattern)) >= threshold

    def _actions_similar(self, a1: dict, a2: dict) -> bool:
        """Check if two actions are similar"""
        return (a1['action_type'] == a2['action_type'] and
                a1.get('target') == a2.get('target') and
                a1.get('location') == a2.get('location'))

    def _action_to_dict(self, action: ObservedAction) -> dict:
        """Convert ObservedAction to dict"""
        return {
            'action_type': action.action_type,
            'target': action.target,
            'location': action.location
        }

    def get_learned_task(self, task_name: str) -> TaskPattern | None:
        """Retrieve learned task pattern"""
        return self.learned_tasks.get(task_name)

    def generate_decomposition_code(self, task_name: str) -> str:
        """Generate Python code for learned task decomposition"""
        pattern = self.learned_tasks.get(task_name)
        if not pattern:
            return ""

        code = f"def _decompose_{task_name}(self, state: WorldState, params: dict) -> list:\n"
        code += f'    """Auto-generated from {pattern.observation_count} observations (confidence: {pattern.confidence:.2f})"""\n'
        code += "    return [\n"

        for action in pattern.action_sequence:
            target = f"'{action['target']}'" if action.get('target') else 'None'
            location = f"'{action['location']}'" if action.get('location') else 'None'
            code += f"        {{'task': '{action['action_type']}', 'params': {{'target': {target}, 'location': {location}}}}},\n"

        code += "    ]\n"
        return code

    def save_learned_tasks(self, filepath: str):
        """Persist learned tasks to disk"""
        data = {
            task_name: {
                'action_sequence': pattern.action_sequence,
                'preconditions': pattern.preconditions,
                'success_rate': pattern.success_rate,
                'observation_count': pattern.observation_count,
                'confidence': pattern.confidence
            }
            for task_name, pattern in self.learned_tasks.items()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_learned_tasks(self, filepath: str):
        """Load learned tasks from disk"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            for task_name, task_data in data.items():
                self.learned_tasks[task_name] = TaskPattern(
                    task_name=task_name,
                    action_sequence=task_data['action_sequence'],
                    preconditions=task_data['preconditions'],
                    success_rate=task_data['success_rate'],
                    observation_count=task_data['observation_count'],
                    confidence=task_data['confidence']
                )
        except FileNotFoundError:
            pass
