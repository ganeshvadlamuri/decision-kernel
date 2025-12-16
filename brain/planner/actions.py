from dataclasses import dataclass, field


@dataclass
class Action:
    """Primitive action representation (v1.0)"""
    action_type: str
    target: str | None = None
    location: str | None = None
    parameters: dict = field(default_factory=dict)
    version: str = "1.0"

    def __str__(self) -> str:
        parts = [self.action_type]
        if self.target:
            parts.append(f"(object={self.target})")
        if self.location:
            parts.append(f"(location={self.location})")
        return "".join(parts)
