"""Decision Kernel skill template"""

from brain.skills.skill import Skill


def create_my_skill() -> Skill:
    """Create custom skill"""
    return Skill(
        name="my_skill",
        description="[DESCRIBE YOUR SKILL]",
        intent_pattern="[INTENT PATTERN]",  # e.g., "bring {target}"
        action_sequence=[
            {"type": "navigate_to", "location": "{target_location}"},
            {"type": "grasp", "target": "{target}"},
            {"type": "navigate_to", "location": "{human_location}"},
            {"type": "release", "target": "{target}"},
        ],
        preconditions=["robot_operational", "target_visible"],
        postconditions=["target_delivered"],
    )
