"""Temporal Paradox Resolution - Plan backwards from desired future state."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from brain.planner.actions import Action


@dataclass
class TimedAction:
    action: Action
    start_time: datetime
    duration: timedelta
    dependencies: list[str]


@dataclass
class TemporalPlan:
    actions: list[TimedAction]
    start_time: datetime
    end_time: datetime
    critical_path: list[str]


class TemporalPlanner:
    def __init__(self):
        self.action_durations = {
            "navigate": timedelta(minutes=5),
            "grasp": timedelta(seconds=30),
            "release": timedelta(seconds=10),
            "brew_coffee": timedelta(minutes=8),
            "heat_water": timedelta(minutes=3),
            "grind_beans": timedelta(minutes=2),
            "pour": timedelta(seconds=30),
            "scan": timedelta(seconds=5),
            "charge": timedelta(minutes=30)
        }

    def reverse_temporal_planning(
        self,
        desired_state: str,
        desired_time: datetime,
        current_state: str | None = None
    ) -> TemporalPlan:
        """Plan backwards from desired future state."""
        # Parse desired state to extract goal
        if "coffee delivered" in desired_state.lower():
            return self._plan_coffee_delivery(desired_time)
        elif "package delivered" in desired_state.lower():
            return self._plan_package_delivery(desired_time)
        else:
            return self._plan_generic_task(desired_state, desired_time)

    def _plan_coffee_delivery(self, desired_time: datetime) -> TemporalPlan:
        """Plan coffee delivery working backwards from deadline."""
        actions_reverse = [
            ("release", "coffee", None, []),
            ("navigate", None, "human", ["release"]),
            ("grasp", "coffee", None, ["navigate"]),
            ("pour", "coffee", None, ["grasp"]),
            ("brew_coffee", "coffee", None, ["pour"]),
            ("grind_beans", "beans", None, ["brew_coffee"]),
            ("heat_water", "water", None, ["brew_coffee"]),
            ("navigate", None, "kitchen", ["grind_beans", "heat_water"])
        ]

        # Calculate backwards from desired_time
        current_time = desired_time
        timed_actions: list[TimedAction] = []

        for action_name, target, location, deps in actions_reverse:
            duration = self.action_durations.get(action_name, timedelta(minutes=1))
            start_time = current_time - duration

            timed_actions.insert(0, TimedAction(
                action=Action(action_type=action_name, target=target, location=location, parameters={}),
                start_time=start_time,
                duration=duration,
                dependencies=deps
            ))

            current_time = start_time

        return TemporalPlan(
            actions=timed_actions,
            start_time=timed_actions[0].start_time,
            end_time=desired_time,
            critical_path=[ta.action.action_type for ta in timed_actions]
        )

    def _plan_package_delivery(self, desired_time: datetime) -> TemporalPlan:
        """Plan package delivery working backwards."""
        actions_reverse = [
            ("release", "package", None, []),
            ("navigate", None, "destination", ["release"]),
            ("grasp", "package", None, ["navigate"]),
            ("navigate", None, "package_location", ["grasp"])
        ]

        current_time = desired_time
        timed_actions: list[TimedAction] = []

        for action_name, target, location, deps in actions_reverse:
            duration = self.action_durations.get(action_name, timedelta(minutes=1))
            start_time = current_time - duration

            timed_actions.insert(0, TimedAction(
                action=Action(action_type=action_name, target=target, location=location, parameters={}),
                start_time=start_time,
                duration=duration,
                dependencies=deps
            ))

            current_time = start_time

        return TemporalPlan(
            actions=timed_actions,
            start_time=timed_actions[0].start_time,
            end_time=desired_time,
            critical_path=[ta.action.action_type for ta in timed_actions]
        )

    def _plan_generic_task(self, desired_state: str, desired_time: datetime) -> TemporalPlan:
        """Generic temporal planning."""
        action = Action(action_type="achieve", target=desired_state, parameters={})
        duration = timedelta(minutes=10)
        start_time = desired_time - duration

        timed_action = TimedAction(
            action=action,
            start_time=start_time,
            duration=duration,
            dependencies=[]
        )

        return TemporalPlan(
            actions=[timed_action],
            start_time=start_time,
            end_time=desired_time,
            critical_path=["achieve"]
        )

    def optimize_timeline(self, plan: TemporalPlan) -> TemporalPlan:
        """Compress timeline by parallelizing independent actions."""
        # Find actions that can run in parallel
        optimized_actions: list[TimedAction] = []
        time_saved = timedelta(0)

        for i, action in enumerate(plan.actions):
            if i > 0 and not action.dependencies:
                # Can run in parallel with previous action
                prev_action = optimized_actions[-1]
                action.start_time = prev_action.start_time
                time_saved += action.duration

            optimized_actions.append(action)

        new_end_time = plan.end_time - time_saved

        return TemporalPlan(
            actions=optimized_actions,
            start_time=plan.start_time,
            end_time=new_end_time,
            critical_path=plan.critical_path
        )

    def detect_conflicts(self, plan: TemporalPlan) -> list[str]:
        """Detect temporal conflicts in plan."""
        conflicts = []

        for i, action1 in enumerate(plan.actions):
            for action2 in plan.actions[i+1:]:
                # Check for time overlap
                if (action1.start_time <= action2.start_time < action1.start_time + action1.duration):
                    conflicts.append(
                        f"Conflict: {action1.action.action_type} and {action2.action.action_type} overlap"
                    )

        return conflicts
