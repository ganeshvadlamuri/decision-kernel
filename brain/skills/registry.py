from brain.skills.skill import Skill


class SkillRegistry:
    """Registry for managing available skills"""

    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a skill by name"""
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        """Retrieve a skill by name"""
        return self._skills.get(name)

    def list(self) -> list[str]:
        """List all registered skill names"""
        return list(self._skills.keys())
