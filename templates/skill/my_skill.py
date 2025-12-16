"""Minimal skill template"""

from brain.skills.skill import Skill


def create_my_skill() -> Skill:
    """
    Create a custom skill

    Replace this with your skill logic:
    - Define the behavior name
    - Specify required inputs
    - List preconditions
    - Define expected effects
    - Create action sequence with parameter substitution
    """
    return Skill(
        name="my_skill",
        description="Description of what this skill does",
        inputs={
            "target": "object to manipulate",
            "destination": "where to move it",
        },
        preconditions=[
            "target exists",
            "target is reachable",
            "destination is valid",
        ],
        effects=[
            "target at destination",
        ],
        action_sequence=[
            {"type": "navigate_to", "location": "{target_location}"},
            {"type": "grasp", "target": "{target}"},
            {"type": "navigate_to", "location": "{destination}"},
            {"type": "release", "target": "{target}"},
        ],
    )
