from dataclasses import dataclass, field


@dataclass
class Skill:
    """Reusable skill definition for complex behaviors"""

    name: str
    description: str
    inputs: dict[str, str] = field(default_factory=dict)
    preconditions: list[str] = field(default_factory=list)
    effects: list[str] = field(default_factory=list)
    action_sequence: list[dict[str, str]] = field(default_factory=list)
