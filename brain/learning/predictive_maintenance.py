"""Predictive Failure Prevention - Predict and prevent failures before they happen"""
import random
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ComponentHealth:
    """Health status of robot component"""
    component_name: str
    health_score: float  # 0.0 to 1.0
    wear_level: float  # 0.0 to 1.0
    usage_hours: float
    last_maintenance: float
    failure_probability_24h: float
    failure_probability_7d: float
    recommended_action: str | None


@dataclass
class SensorReading:
    """Sensor reading for predictive analysis"""
    sensor_name: str
    value: float
    timestamp: float
    expected_value: float
    drift: float


@dataclass
class MaintenanceSchedule:
    """Scheduled maintenance task"""
    component: str
    urgency: str  # 'critical', 'high', 'medium', 'low'
    estimated_time: float
    failure_risk: float
    scheduled_time: float | None = None


class PredictiveMaintenanceSystem:
    """Predicts failures and schedules preventive maintenance"""
    
    def __init__(self):
        self.components: dict[str, ComponentHealth] = {}
        self.sensor_history: dict[str, list[SensorReading]] = {}
        self.maintenance_history: list[dict] = []
        self.failure_models: dict[str, dict] = self._initialize_failure_models()
        
        # Initialize common robot components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize robot components"""
        components = [
            'grasp_motor', 'navigation_motor', 'battery', 
            'camera', 'lidar', 'gripper', 'wheels'
        ]
        
        for comp in components:
            self.components[comp] = ComponentHealth(
                component_name=comp,
                health_score=1.0,
                wear_level=0.0,
                usage_hours=0.0,
                last_maintenance=time.time(),
                failure_probability_24h=0.0,
                failure_probability_7d=0.0,
                recommended_action=None
            )
    
    def _initialize_failure_models(self) -> dict[str, dict]:
        """Initialize failure prediction models for components"""
        return {
            'grasp_motor': {
                'wear_rate': 0.001,  # per hour
                'failure_threshold': 0.7,
                'critical_drift': 0.15
            },
            'navigation_motor': {
                'wear_rate': 0.0008,
                'failure_threshold': 0.65,
                'critical_drift': 0.12
            },
            'battery': {
                'wear_rate': 0.0005,
                'failure_threshold': 0.5,
                'critical_drift': 0.20
            },
            'camera': {
                'wear_rate': 0.0003,
                'failure_threshold': 0.6,
                'critical_drift': 0.10
            },
            'lidar': {
                'wear_rate': 0.0004,
                'failure_threshold': 0.6,
                'critical_drift': 0.10
            },
            'gripper': {
                'wear_rate': 0.0012,
                'failure_threshold': 0.75,
                'critical_drift': 0.18
            },
            'wheels': {
                'wear_rate': 0.0006,
                'failure_threshold': 0.65,
                'critical_drift': 0.15
            }
        }
    
    def record_sensor_reading(self, sensor_name: str, value: float, expected_value: float):
        """Record sensor reading for drift analysis"""
        drift = abs(value - expected_value) / expected_value if expected_value != 0 else 0
        
        reading = SensorReading(
            sensor_name=sensor_name,
            value=value,
            timestamp=time.time(),
            expected_value=expected_value,
            drift=drift
        )
        
        if sensor_name not in self.sensor_history:
            self.sensor_history[sensor_name] = []
        
        self.sensor_history[sensor_name].append(reading)
        
        # Keep only recent history (last 1000 readings)
        if len(self.sensor_history[sensor_name]) > 1000:
            self.sensor_history[sensor_name] = self.sensor_history[sensor_name][-1000:]
    
    def update_component_usage(self, component: str, hours_used: float):
        """Update component usage hours"""
        if component in self.components:
            comp = self.components[component]
            comp.usage_hours += hours_used
            
            # Update wear level
            model = self.failure_models.get(component, {})
            wear_rate = model.get('wear_rate', 0.001)
            comp.wear_level = min(comp.wear_level + (hours_used * wear_rate), 1.0)
            
            # Update health score
            comp.health_score = 1.0 - comp.wear_level
            
            # Predict failure probability
            self._update_failure_predictions(component)
    
    def _update_failure_predictions(self, component: str):
        """Update failure probability predictions"""
        comp = self.components[component]
        model = self.failure_models.get(component, {})
        
        # Base probability from wear level
        wear_factor = comp.wear_level
        
        # Adjust for sensor drift
        drift_factor = self._calculate_drift_factor(component)
        
        # Adjust for time since maintenance
        time_since_maintenance = time.time() - comp.last_maintenance
        maintenance_factor = min(time_since_maintenance / (365 * 24 * 3600), 0.3)  # Max 30% from age
        
        # Combined failure probability
        base_prob = wear_factor * 0.5 + drift_factor * 0.3 + maintenance_factor * 0.2
        
        # 24-hour probability
        comp.failure_probability_24h = min(base_prob * 0.1, 1.0)
        
        # 7-day probability
        comp.failure_probability_7d = min(base_prob * 0.5, 1.0)
        
        # Recommend action
        if comp.failure_probability_24h > 0.7:
            comp.recommended_action = 'IMMEDIATE_MAINTENANCE'
        elif comp.failure_probability_7d > 0.5:
            comp.recommended_action = 'SCHEDULE_MAINTENANCE'
        elif comp.wear_level > 0.6:
            comp.recommended_action = 'MONITOR_CLOSELY'
        else:
            comp.recommended_action = None
    
    def _calculate_drift_factor(self, component: str) -> float:
        """Calculate drift factor from sensor readings"""
        sensor_name = f"{component}_sensor"
        
        if sensor_name not in self.sensor_history:
            return 0.0
        
        recent_readings = self.sensor_history[sensor_name][-100:]
        
        if not recent_readings:
            return 0.0
        
        avg_drift = sum(r.drift for r in recent_readings) / len(recent_readings)
        
        model = self.failure_models.get(component, {})
        critical_drift = model.get('critical_drift', 0.15)
        
        return min(avg_drift / critical_drift, 1.0)
    
    def predict_failure(self, component: str, hours_ahead: int = 24) -> float:
        """Predict failure probability for component"""
        if component not in self.components:
            return 0.0
        
        comp = self.components[component]
        
        if hours_ahead <= 24:
            return comp.failure_probability_24h
        elif hours_ahead <= 168:  # 7 days
            return comp.failure_probability_7d
        else:
            # Extrapolate for longer periods
            days = hours_ahead / 24
            return min(comp.failure_probability_7d * (days / 7), 1.0)
    
    def schedule_maintenance(self) -> list[MaintenanceSchedule]:
        """Generate maintenance schedule based on predictions"""
        schedule = []
        
        for comp_name, comp in self.components.items():
            if comp.recommended_action:
                urgency = self._determine_urgency(comp)
                
                schedule.append(MaintenanceSchedule(
                    component=comp_name,
                    urgency=urgency,
                    estimated_time=self._estimate_maintenance_time(comp_name),
                    failure_risk=comp.failure_probability_24h,
                    scheduled_time=None
                ))
        
        # Sort by urgency and failure risk
        urgency_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        schedule.sort(key=lambda s: (urgency_order[s.urgency], -s.failure_risk))
        
        return schedule
    
    def _determine_urgency(self, comp: ComponentHealth) -> str:
        """Determine maintenance urgency"""
        if comp.failure_probability_24h > 0.7:
            return 'critical'
        elif comp.failure_probability_24h > 0.4:
            return 'high'
        elif comp.failure_probability_7d > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_maintenance_time(self, component: str) -> float:
        """Estimate maintenance time in minutes"""
        times = {
            'grasp_motor': 30,
            'navigation_motor': 45,
            'battery': 60,
            'camera': 20,
            'lidar': 25,
            'gripper': 35,
            'wheels': 40
        }
        return times.get(component, 30)
    
    def perform_maintenance(self, component: str):
        """Record maintenance performed"""
        if component in self.components:
            comp = self.components[component]
            comp.last_maintenance = time.time()
            comp.wear_level = max(comp.wear_level - 0.5, 0.0)  # Reduce wear
            comp.health_score = 1.0 - comp.wear_level
            comp.recommended_action = None
            
            self.maintenance_history.append({
                'component': component,
                'timestamp': time.time(),
                'wear_before': comp.wear_level + 0.5,
                'wear_after': comp.wear_level
            })
            
            # Recalculate predictions
            self._update_failure_predictions(component)
    
    def get_health_report(self) -> dict[str, Any]:
        """Generate comprehensive health report"""
        critical_components = [
            comp for comp in self.components.values()
            if comp.failure_probability_24h > 0.5
        ]
        
        avg_health = sum(c.health_score for c in self.components.values()) / len(self.components)
        
        return {
            'overall_health': avg_health,
            'critical_components': len(critical_components),
            'components_needing_maintenance': sum(
                1 for c in self.components.values() if c.recommended_action
            ),
            'total_components': len(self.components),
            'maintenance_schedule': self.schedule_maintenance(),
            'component_details': {
                name: {
                    'health': comp.health_score,
                    'wear': comp.wear_level,
                    'failure_24h': comp.failure_probability_24h,
                    'action': comp.recommended_action
                }
                for name, comp in self.components.items()
            }
        }
    
    def simulate_wear(self, hours: float):
        """Simulate component wear over time (for testing)"""
        for component in self.components:
            self.update_component_usage(component, hours)
            
            # Simulate sensor drift
            sensor_name = f"{component}_sensor"
            expected = 100.0
            actual = expected + random.uniform(-20, 20) * (self.components[component].wear_level)
            self.record_sensor_reading(sensor_name, actual, expected)
