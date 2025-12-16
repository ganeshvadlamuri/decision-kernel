"""Extended WorldState with obstacle detection, battery level, and emergency monitoring"""
from dataclasses import dataclass, field

from brain.world.state import WorldState


@dataclass
class ExtendedWorldState(WorldState):
    """Enhanced world state with real-time monitoring capabilities"""

    # Battery and power
    battery_level: float = 100.0  # 0-100%
    charging: bool = False
    power_consumption_rate: float = 1.0  # % per minute

    # Obstacles and navigation
    detected_obstacles: list[dict] = field(default_factory=list)
    blocked_paths: dict[str, bool] = field(default_factory=dict)
    alternative_routes: dict[str, list[str]] = field(default_factory=dict)

    # Door states
    door_states: dict[str, str] = field(default_factory=dict)  # location -> 'open'/'closed'/'locked'

    # Emergency detection
    fire_detected: bool = False
    fire_location: str | None = None
    intrusion_detected: bool = False
    intrusion_location: str | None = None
    fall_detected: bool = False

    # Environmental context
    time_of_day: str = "day"  # 'morning'/'afternoon'/'evening'/'night'
    human_present: bool = True
    noise_level: float = 0.0  # 0-100 dB
    temperature: float = 22.0  # Celsius

    # Object tracking
    missing_objects: list[str] = field(default_factory=list)
    object_weights: dict[str, float] = field(default_factory=dict)  # kg

    def is_path_blocked(self, location: str) -> bool:
        """Check if path to location is blocked"""
        return self.blocked_paths.get(location, False)

    def is_door_open(self, location: str) -> bool:
        """Check if door at location is open"""
        return self.door_states.get(location, 'open') == 'open'

    def is_door_locked(self, location: str) -> bool:
        """Check if door at location is locked"""
        return self.door_states.get(location, 'open') == 'locked'

    def needs_charging(self, threshold: float = 20.0) -> bool:
        """Check if battery needs charging"""
        return self.battery_level < threshold and not self.charging

    def has_emergency(self) -> bool:
        """Check if any emergency condition exists"""
        return self.fire_detected or self.intrusion_detected or self.fall_detected

    def get_emergency_type(self) -> str | None:
        """Get type of emergency"""
        if self.fire_detected:
            return 'fire'
        if self.intrusion_detected:
            return 'intrusion'
        if self.fall_detected:
            return 'fall'
        return None

    def add_obstacle(self, location: str, obstacle_type: str, position: dict):
        """Record detected obstacle"""
        self.detected_obstacles.append({
            'location': location,
            'type': obstacle_type,
            'position': position,
            'timestamp': self.timestamp
        })
        self.blocked_paths[location] = True

    def clear_obstacle(self, location: str):
        """Clear obstacle from location"""
        self.blocked_paths[location] = False
        self.detected_obstacles = [
            obs for obs in self.detected_obstacles
            if obs['location'] != location
        ]

    def set_door_state(self, location: str, state: str):
        """Set door state (open/closed/locked)"""
        self.door_states[location] = state

    def trigger_emergency(self, emergency_type: str, location: str | None = None):
        """Trigger emergency condition"""
        if emergency_type == 'fire':
            self.fire_detected = True
            self.fire_location = location
        elif emergency_type == 'intrusion':
            self.intrusion_detected = True
            self.intrusion_location = location
        elif emergency_type == 'fall':
            self.fall_detected = True

    def clear_emergency(self, emergency_type: str):
        """Clear emergency condition"""
        if emergency_type == 'fire':
            self.fire_detected = False
            self.fire_location = None
        elif emergency_type == 'intrusion':
            self.intrusion_detected = False
            self.intrusion_location = None
        elif emergency_type == 'fall':
            self.fall_detected = False

    def update_battery(self, delta_time: float):
        """Update battery level based on time elapsed"""
        if self.charging:
            self.battery_level = min(100.0, self.battery_level + delta_time * 10.0)  # 10% per minute charging
        else:
            self.battery_level = max(0.0, self.battery_level - delta_time * self.power_consumption_rate)

    def mark_object_missing(self, object_name: str):
        """Mark object as missing"""
        if object_name not in self.missing_objects:
            self.missing_objects.append(object_name)

    def mark_object_found(self, object_name: str):
        """Mark object as found"""
        if object_name in self.missing_objects:
            self.missing_objects.remove(object_name)

    def is_object_too_heavy(self, object_name: str, max_weight: float = 5.0) -> bool:
        """Check if object exceeds weight limit"""
        weight = self.object_weights.get(object_name, 0.0)
        return weight > max_weight

    def get_context(self) -> dict:
        """Get current context for decision making"""
        return {
            'battery_level': self.battery_level,
            'time_of_day': self.time_of_day,
            'human_present': self.human_present,
            'emergency': self.has_emergency(),
            'emergency_type': self.get_emergency_type(),
            'charging': self.charging
        }
