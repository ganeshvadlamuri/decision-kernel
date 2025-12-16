import time
from dataclasses import dataclass, field

from brain.world.objects import WorldObject


@dataclass
class WorldState:
    """Container for world representation (v1.0)"""
    objects: list[WorldObject] = field(default_factory=list)
    robot_location: str = "unknown"
    human_location: str = "unknown"
    locations: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    frame_id: str = "world"
    relations: dict = field(default_factory=dict)

    def get_object(self, name: str) -> WorldObject | None:
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def get_objects_at(self, location: str) -> list[WorldObject]:
        return [obj for obj in self.objects if obj.location == location]
