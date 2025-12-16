"""Swarm Intelligence - Collective learning across multiple robots"""
import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SwarmKnowledge:
    """Shared knowledge across robot swarm"""
    knowledge_type: str
    content: dict[str, Any]
    source_robot_id: str
    timestamp: float
    confidence: float
    verified_by: list[str] = field(default_factory=list)


@dataclass
class SwarmRobot:
    """Individual robot in swarm"""
    robot_id: str
    location: str
    battery_level: float
    status: str
    last_update: float


class SwarmIntelligence:
    """Collective intelligence system for robot swarms"""
    
    def __init__(self, robot_id: str, swarm_size: int = 100):
        self.robot_id = robot_id
        self.swarm_size = swarm_size
        self.shared_knowledge: dict[str, SwarmKnowledge] = {}
        self.swarm_robots: dict[str, SwarmRobot] = {}
        self.broadcast_history: list[dict] = []
        
        # Initialize self
        self.swarm_robots[robot_id] = SwarmRobot(
            robot_id=robot_id,
            location='unknown',
            battery_level=100.0,
            status='active',
            last_update=time.time()
        )
    
    def broadcast(self, knowledge_type: str, content: dict[str, Any], confidence: float = 1.0):
        """Broadcast knowledge to entire swarm"""
        knowledge = SwarmKnowledge(
            knowledge_type=knowledge_type,
            content=content,
            source_robot_id=self.robot_id,
            timestamp=time.time(),
            confidence=confidence,
            verified_by=[self.robot_id]
        )
        
        # Store in shared knowledge
        key = f"{knowledge_type}:{json.dumps(content, sort_keys=True)}"
        self.shared_knowledge[key] = knowledge
        
        # Record broadcast
        self.broadcast_history.append({
            'type': knowledge_type,
            'content': content,
            'timestamp': knowledge.timestamp,
            'robot_id': self.robot_id
        })
        
        # Simulate instant propagation to all robots
        return self._propagate_to_swarm(knowledge)
    
    def _propagate_to_swarm(self, knowledge: SwarmKnowledge) -> dict[str, Any]:
        """Simulate knowledge propagation across swarm"""
        # In real implementation, this would use:
        # - Mesh network
        # - Cloud sync
        # - Direct robot-to-robot communication
        
        propagation_time = 0.001 * self.swarm_size  # 1ms per robot
        robots_reached = min(self.swarm_size, len(self.swarm_robots) * 10)
        
        return {
            'knowledge_type': knowledge.knowledge_type,
            'robots_reached': robots_reached,
            'propagation_time': propagation_time,
            'timestamp': knowledge.timestamp
        }
    
    def query(self, knowledge_type: str, context: dict[str, Any] | None = None) -> list[SwarmKnowledge]:
        """Query swarm knowledge"""
        results = []
        
        for key, knowledge in self.shared_knowledge.items():
            if knowledge.knowledge_type == knowledge_type:
                # Filter by context if provided
                if context:
                    if self._context_matches(knowledge.content, context):
                        results.append(knowledge)
                else:
                    results.append(knowledge)
        
        # Sort by confidence and verification count
        results.sort(
            key=lambda k: (k.confidence, len(k.verified_by)),
            reverse=True
        )
        
        return results
    
    def verify_knowledge(self, knowledge_key: str):
        """Verify knowledge from another robot"""
        if knowledge_key in self.shared_knowledge:
            knowledge = self.shared_knowledge[knowledge_key]
            if self.robot_id not in knowledge.verified_by:
                knowledge.verified_by.append(self.robot_id)
                
                # Increase confidence with more verifications
                verification_boost = 0.1 * len(knowledge.verified_by)
                knowledge.confidence = min(knowledge.confidence + verification_boost, 1.0)
    
    def learn_from_swarm(self, knowledge_type: str) -> dict[str, Any]:
        """Learn from collective swarm experience"""
        relevant_knowledge = self.query(knowledge_type)
        
        if not relevant_knowledge:
            return {'learned': False, 'reason': 'no_knowledge_available'}
        
        # Aggregate knowledge from multiple sources
        aggregated = self._aggregate_knowledge(relevant_knowledge)
        
        return {
            'learned': True,
            'knowledge_type': knowledge_type,
            'sources': len(relevant_knowledge),
            'confidence': aggregated['confidence'],
            'content': aggregated['content']
        }
    
    def _aggregate_knowledge(self, knowledge_list: list[SwarmKnowledge]) -> dict[str, Any]:
        """Aggregate knowledge from multiple robots"""
        if not knowledge_list:
            return {'confidence': 0.0, 'content': {}}
        
        # Weighted average by confidence and verification count
        total_weight = 0.0
        aggregated_content = {}
        
        for k in knowledge_list:
            weight = k.confidence * (1 + len(k.verified_by) * 0.1)
            total_weight += weight
            
            # Merge content
            for key, value in k.content.items():
                if key not in aggregated_content:
                    aggregated_content[key] = []
                aggregated_content[key].append((value, weight))
        
        # Calculate weighted averages
        final_content = {}
        for key, values in aggregated_content.items():
            if isinstance(values[0][0], (int, float)):
                weighted_sum = sum(v * w for v, w in values)
                final_content[key] = weighted_sum / total_weight
            else:
                # For non-numeric, take most common
                final_content[key] = max(values, key=lambda x: x[1])[0]
        
        avg_confidence = sum(k.confidence for k in knowledge_list) / len(knowledge_list)
        
        return {
            'confidence': avg_confidence,
            'content': final_content
        }
    
    def report_status(self, location: str, battery_level: float, status: str):
        """Report robot status to swarm"""
        self.swarm_robots[self.robot_id] = SwarmRobot(
            robot_id=self.robot_id,
            location=location,
            battery_level=battery_level,
            status=status,
            last_update=time.time()
        )
    
    def get_swarm_status(self) -> dict[str, Any]:
        """Get status of entire swarm"""
        active_robots = [r for r in self.swarm_robots.values() if r.status == 'active']
        
        if not active_robots:
            return {'active_robots': 0}
        
        avg_battery = sum(r.battery_level for r in active_robots) / len(active_robots)
        
        return {
            'total_robots': len(self.swarm_robots),
            'active_robots': len(active_robots),
            'avg_battery': avg_battery,
            'locations': list(set(r.location for r in active_robots)),
            'shared_knowledge_items': len(self.shared_knowledge)
        }
    
    def find_nearest_robot(self, location: str, capability: str | None = None) -> SwarmRobot | None:
        """Find nearest robot with optional capability"""
        # Simplified: just return first active robot
        # Real implementation would use actual distances
        for robot in self.swarm_robots.values():
            if robot.status == 'active' and robot.battery_level > 20:
                return robot
        return None
    
    def coordinate_task(self, task_type: str, requirements: dict[str, Any]) -> dict[str, Any]:
        """Coordinate task across multiple robots"""
        # Find suitable robots
        suitable_robots = [
            r for r in self.swarm_robots.values()
            if r.status == 'active' and r.battery_level > 30
        ]
        
        if not suitable_robots:
            return {'success': False, 'reason': 'no_available_robots'}
        
        # Assign task to robots
        num_robots_needed = requirements.get('robots_needed', 1)
        assigned_robots = suitable_robots[:num_robots_needed]
        
        return {
            'success': True,
            'task_type': task_type,
            'assigned_robots': [r.robot_id for r in assigned_robots],
            'estimated_completion': requirements.get('duration', 60)
        }
    
    def _context_matches(self, content: dict, context: dict) -> bool:
        """Check if content matches context"""
        for key, value in context.items():
            if key in content and content[key] != value:
                return False
        return True
    
    def get_collective_experience(self, task_type: str) -> dict[str, Any]:
        """Get collective experience from all robots"""
        experiences = self.query(f"experience_{task_type}")
        
        if not experiences:
            return {'total_attempts': 0, 'success_rate': 0.0}
        
        total_attempts = sum(
            exp.content.get('attempts', 0) 
            for exp in experiences
        )
        
        total_successes = sum(
            exp.content.get('successes', 0)
            for exp in experiences
        )
        
        return {
            'total_attempts': total_attempts,
            'success_rate': total_successes / total_attempts if total_attempts > 0 else 0.0,
            'contributing_robots': len(experiences),
            'avg_confidence': sum(exp.confidence for exp in experiences) / len(experiences)
        }
