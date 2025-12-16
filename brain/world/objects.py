from dataclasses import dataclass


@dataclass
class WorldObject:
    """Representation of an object in the world"""
    name: str
    location: str
    object_type: str
    graspable: bool = True
    position: tuple | None = None
