"""Spatial reasoning - Understand 3D relationships."""

from dataclasses import dataclass
from typing import Any
import math


@dataclass
class Position:
    """3D position."""

    x: float
    y: float
    z: float


@dataclass
class SpatialObject:
    """Object with spatial properties."""

    name: str
    position: Position
    size: tuple[float, float, float]  # width, height, depth


class SpatialReasoner:
    """Understand 3D relationships ('behind', 'inside', 'next to')."""

    def __init__(self) -> None:
        self.objects: dict[str, SpatialObject] = {}

    def add_object(self, name: str, x: float, y: float, z: float, size: tuple[float, float, float]) -> None:
        """Add object to spatial model."""
        self.objects[name] = SpatialObject(name, Position(x, y, z), size)

    def is_behind(self, obj1: str, obj2: str, reference_direction: str = "north") -> bool:
        """Check if obj1 is behind obj2."""
        if obj1 not in self.objects or obj2 not in self.objects:
            return False

        o1 = self.objects[obj1]
        o2 = self.objects[obj2]

        # Behind means further in opposite direction
        if reference_direction == "north":
            return o1.position.y < o2.position.y
        return False

    def is_in_front(self, obj1: str, obj2: str, reference_direction: str = "north") -> bool:
        """Check if obj1 is in front of obj2."""
        return self.is_behind(obj2, obj1, reference_direction)

    def is_next_to(self, obj1: str, obj2: str, threshold: float = 2.0) -> bool:
        """Check if obj1 is next to obj2."""
        if obj1 not in self.objects or obj2 not in self.objects:
            return False

        distance = self.distance(obj1, obj2)
        return distance <= threshold

    def is_inside(self, obj1: str, container: str) -> bool:
        """Check if obj1 is inside container."""
        if obj1 not in self.objects or container not in self.objects:
            return False

        o1 = self.objects[obj1]
        cont = self.objects[container]

        # Simple bounding box check
        return (
            abs(o1.position.x - cont.position.x) < cont.size[0] / 2
            and abs(o1.position.y - cont.position.y) < cont.size[1] / 2
            and abs(o1.position.z - cont.position.z) < cont.size[2] / 2
        )

    def is_on_top(self, obj1: str, obj2: str, threshold: float = 0.5) -> bool:
        """Check if obj1 is on top of obj2."""
        if obj1 not in self.objects or obj2 not in self.objects:
            return False

        o1 = self.objects[obj1]
        o2 = self.objects[obj2]

        # Above and close in x,y
        z_above = o1.position.z > o2.position.z
        xy_close = (
            abs(o1.position.x - o2.position.x) < threshold
            and abs(o1.position.y - o2.position.y) < threshold
        )

        return z_above and xy_close

    def distance(self, obj1: str, obj2: str) -> float:
        """Calculate distance between objects."""
        if obj1 not in self.objects or obj2 not in self.objects:
            return float("inf")

        o1 = self.objects[obj1]
        o2 = self.objects[obj2]

        return math.sqrt(
            (o1.position.x - o2.position.x) ** 2
            + (o1.position.y - o2.position.y) ** 2
            + (o1.position.z - o2.position.z) ** 2
        )

    def find_nearest(self, obj: str) -> str | None:
        """Find nearest object to obj."""
        if obj not in self.objects:
            return None

        nearest = None
        min_distance = float("inf")

        for other in self.objects:
            if other == obj:
                continue
            dist = self.distance(obj, other)
            if dist < min_distance:
                min_distance = dist
                nearest = other

        return nearest

    def get_spatial_relations(self, obj: str) -> dict[str, Any]:
        """Get all spatial relations for object."""
        if obj not in self.objects:
            return {}

        relations = {
            "next_to": [],
            "inside": [],
            "on_top_of": [],
            "nearest": self.find_nearest(obj),
        }

        for other in self.objects:
            if other == obj:
                continue

            if self.is_next_to(obj, other):
                relations["next_to"].append(other)
            if self.is_inside(obj, other):
                relations["inside"].append(other)
            if self.is_on_top(obj, other):
                relations["on_top_of"].append(other)

        return relations
