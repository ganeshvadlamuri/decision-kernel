from dataclasses import dataclass


@dataclass
class Goal:
    """Structured representation of human intent"""
    action: str
    target: str | None = None
    location: str | None = None
    recipient: str | None = None
