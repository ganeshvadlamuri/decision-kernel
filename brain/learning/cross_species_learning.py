"""Cross-Species Learning - Learn from animal behaviors."""
from dataclasses import dataclass
from typing import Dict, List
from brain.planner.actions import Action


@dataclass
class AnimalBehavior:
    species: str
    behavior: str
    principle: str
    robot_translation: List[Action]


class CrossSpeciesLearning:
    def __init__(self):
        self.behaviors: Dict[str, Dict[str, AnimalBehavior]] = {
            "dog": {
                "obstacle_avoidance": AnimalBehavior(
                    species="dog",
                    behavior="obstacle_avoidance",
                    principle="Sniff and circle around obstacles",
                    robot_translation=[
                        Action(action_type="scan", target="obstacle", parameters={"range": 2.0}),
                        Action(action_type="calculate_path", target="around", parameters={"clearance": 0.5}),
                        Action(action_type="navigate", location="alternate_route", parameters={"speed": "moderate"})
                    ]
                ),
                "pack_coordination": AnimalBehavior(
                    species="dog",
                    behavior="pack_coordination",
                    principle="Follow leader, maintain formation",
                    robot_translation=[
                        Action(action_type="identify_leader", target="robot", parameters={}),
                        Action(action_type="maintain_distance", target="leader", parameters={"distance": 1.0}),
                        Action(action_type="sync_movement", target="formation", parameters={})
                    ]
                )
            },
            "cat": {
                "stealth": AnimalBehavior(
                    species="cat",
                    behavior="stealth",
                    principle="Move slowly, minimize noise",
                    robot_translation=[
                        Action(action_type="reduce_speed", target="motors", parameters={"speed": 0.2}),
                        Action(action_type="minimize_vibration", target="actuators", parameters={}),
                        Action(action_type="navigate", location="destination", parameters={"mode": "silent"})
                    ]
                ),
                "precision": AnimalBehavior(
                    species="cat",
                    behavior="precision",
                    principle="Calculate exact landing point",
                    robot_translation=[
                        Action(action_type="measure_distance", target="target", parameters={"accuracy": "high"}),
                        Action(action_type="calculate_trajectory", target="path", parameters={}),
                        Action(action_type="execute_precise_movement", location="destination", parameters={})
                    ]
                )
            },
            "bird": {
                "navigation": AnimalBehavior(
                    species="bird",
                    behavior="navigation",
                    principle="Use landmarks and sun position",
                    robot_translation=[
                        Action(action_type="identify_landmarks", target="environment", parameters={}),
                        Action(action_type="calculate_bearing", location="destination", parameters={"method": "visual"}),
                        Action(action_type="navigate", location="destination", parameters={"mode": "landmark_based"})
                    ]
                )
            },
            "ant": {
                "path_optimization": AnimalBehavior(
                    species="ant",
                    behavior="path_optimization",
                    principle="Leave markers, follow shortest path",
                    robot_translation=[
                        Action(action_type="mark_path", location="current_location", parameters={"marker": "virtual"}),
                        Action(action_type="evaluate_path_efficiency", target="route", parameters={}),
                        Action(action_type="optimize_route", location="destination", parameters={"method": "pheromone"})
                    ]
                )
            }
        }
    
    def learn_from_animal_behavior(self, species: str, behavior: str) -> List[Action]:
        """Learn from animal behavior and translate to robot actions."""
        if species not in self.behaviors:
            raise ValueError(f"Unknown species: {species}")
        if behavior not in self.behaviors[species]:
            raise ValueError(f"Unknown behavior for {species}: {behavior}")
        
        animal_behavior = self.behaviors[species][behavior]
        return animal_behavior.robot_translation
    
    def get_principle(self, species: str, behavior: str) -> str:
        """Get the underlying principle of an animal behavior."""
        if species in self.behaviors and behavior in self.behaviors[species]:
            return self.behaviors[species][behavior].principle
        return ""
    
    def list_species(self) -> List[str]:
        """List all available species."""
        return list(self.behaviors.keys())
    
    def list_behaviors(self, species: str) -> List[str]:
        """List all behaviors for a species."""
        if species in self.behaviors:
            return list(self.behaviors[species].keys())
        return []
