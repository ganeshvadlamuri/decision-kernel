"""Built-in reference skills"""

from brain.skills.skill import Skill


def create_bring_water_skill() -> Skill:
    """Reference skill: bring water to human"""
    return Skill(
        name="bring",
        description="Bring an object to the human",
        inputs={"target": "object to bring"},
        preconditions=["object exists", "object is graspable"],
        effects=["object at human location"],
        action_sequence=[
            {"type": "navigate_to", "location": "{target_location}"},
            {"type": "grasp", "target": "{target}"},
            {"type": "navigate_to", "location": "{human_location}"},
            {"type": "release", "target": "{target}"},
        ],
    )
