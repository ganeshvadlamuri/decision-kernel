"""Curiosity-Driven Exploration - Robot explores when idle to learn."""
from dataclasses import dataclass
from typing import List, Dict, Any, Set
from datetime import datetime
import random


@dataclass
class Discovery:
    location: str
    object_found: str
    timestamp: datetime
    novelty_score: float
    description: str


@dataclass
class ExplorationGoal:
    target_area: str
    motivation: str
    expected_learning: str


class CuriosityEngine:
    def __init__(self):
        self.known_areas: Set[str] = {"home", "kitchen", "living_room"}
        self.known_objects: Dict[str, List[str]] = {
            "kitchen": ["fridge", "stove", "sink"],
            "living_room": ["couch", "tv", "table"],
            "home": []
        }
        self.discoveries: List[Discovery] = []
        self.exploration_count = 0
        self.curiosity_level = 0.8
    
    def explore_unknown_areas(self, time_available: int = 300) -> List[Discovery]:
        """Explore environment when idle to learn new things."""
        discoveries = []
        explorations = min(3, time_available // 100)
        
        for _ in range(explorations):
            # Decide what to explore
            goal = self._generate_exploration_goal()
            
            # Explore and discover
            discovery = self._explore_area(goal)
            
            if discovery:
                discoveries.append(discovery)
                self._update_world_model(discovery)
        
        self.exploration_count += explorations
        return discoveries
    
    def _generate_exploration_goal(self) -> ExplorationGoal:
        """Generate curiosity-driven exploration goal."""
        # Explore unknown areas
        possible_areas = ["kitchen", "living_room", "bedroom", "bathroom", "garage", "office"]
        unknown_areas = [a for a in possible_areas if a not in self.known_areas]
        
        if unknown_areas and random.random() < 0.6:
            target = random.choice(unknown_areas)
            return ExplorationGoal(
                target_area=target,
                motivation="discover_new_area",
                expected_learning=f"Learn about {target} layout and objects"
            )
        
        # Re-explore known areas for changes
        known = list(self.known_areas)
        if known:
            target = random.choice(known)
            return ExplorationGoal(
                target_area=target,
                motivation="detect_changes",
                expected_learning=f"Check for new objects or changes in {target}"
            )
        
        return ExplorationGoal(
            target_area="home",
            motivation="general_exploration",
            expected_learning="General environment awareness"
        )
    
    def _explore_area(self, goal: ExplorationGoal) -> Discovery:
        """Explore specific area and make discoveries."""
        area = goal.target_area
        
        # Simulate discovery
        possible_discoveries = {
            "kitchen": ["coffee_machine", "microwave", "toaster", "blender", "dishwasher"],
            "living_room": ["bookshelf", "lamp", "plant", "picture_frame"],
            "bedroom": ["bed", "closet", "desk", "mirror"],
            "bathroom": ["shower", "toilet", "sink", "mirror"],
            "garage": ["tools", "car", "bicycle", "storage_boxes"],
            "office": ["computer", "printer", "desk", "chair"]
        }
        
        # Check if area has undiscovered objects
        known_in_area = self.known_objects.get(area, [])
        possible_in_area = possible_discoveries.get(area, [])
        undiscovered = [obj for obj in possible_in_area if obj not in known_in_area]
        
        if undiscovered:
            discovered_object = random.choice(undiscovered)
            novelty = 0.9 if area not in self.known_areas else 0.6
            
            return Discovery(
                location=area,
                object_found=discovered_object,
                timestamp=datetime.now(),
                novelty_score=novelty,
                description=f"Found {discovered_object} in {area}"
            )
        
        # Discover changes in known areas
        if area in self.known_areas and random.random() < 0.3:
            changes = ["new_coffee_machine", "rearranged_furniture", "new_plant", "different_lighting"]
            change = random.choice(changes)
            
            return Discovery(
                location=area,
                object_found=change,
                timestamp=datetime.now(),
                novelty_score=0.5,
                description=f"Detected change: {change} in {area}"
            )
        
        return None
    
    def _update_world_model(self, discovery: Discovery):
        """Update internal world model with discovery."""
        # Add area to known areas
        self.known_areas.add(discovery.location)
        
        # Add object to known objects
        if discovery.location not in self.known_objects:
            self.known_objects[discovery.location] = []
        
        if discovery.object_found not in self.known_objects[discovery.location]:
            self.known_objects[discovery.location].append(discovery.object_found)
        
        # Store discovery
        self.discoveries.append(discovery)
    
    def should_explore(self, idle_time: int, battery_level: float) -> bool:
        """Decide if robot should explore based on conditions."""
        if battery_level < 0.3:
            return False
        
        if idle_time < 60:
            return False
        
        # Higher curiosity = more likely to explore
        return random.random() < self.curiosity_level
    
    def get_exploration_stats(self) -> Dict[str, Any]:
        """Get statistics on exploration."""
        return {
            "explorations_performed": self.exploration_count,
            "areas_discovered": len(self.known_areas),
            "total_objects_known": sum(len(objs) for objs in self.known_objects.values()),
            "discoveries_made": len(self.discoveries),
            "curiosity_level": self.curiosity_level,
            "avg_novelty": sum(d.novelty_score for d in self.discoveries) / max(1, len(self.discoveries))
        }
    
    def get_recent_discoveries(self, count: int = 5) -> List[Discovery]:
        """Get most recent discoveries."""
        return self.discoveries[-count:] if self.discoveries else []
