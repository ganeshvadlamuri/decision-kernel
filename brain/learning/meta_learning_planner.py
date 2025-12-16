"""Meta-Learning Planner - Planner that improves its own planning algorithm."""
from dataclasses import dataclass
from typing import List, Dict, Any
import time
import ast


@dataclass
class PerformanceMetric:
    planning_time: float
    plan_quality: float
    success_rate: float
    avg_plan_length: float


@dataclass
class CodeOptimization:
    optimization_type: str
    code_change: str
    expected_improvement: float


class MetaLearningPlanner:
    def __init__(self):
        self.performance_history: List[PerformanceMetric] = []
        self.optimization_history: List[CodeOptimization] = []
        self.current_algorithm_version = 1.0
        self.planning_speed_multiplier = 1.0
        self.intelligence_multiplier = 1.0
        
    def record_performance(self, planning_time: float, plan_quality: float, 
                          success_rate: float, plan_length: int):
        """Record performance metrics for analysis."""
        metric = PerformanceMetric(
            planning_time=planning_time,
            plan_quality=plan_quality,
            success_rate=success_rate,
            avg_plan_length=float(plan_length)
        )
        self.performance_history.append(metric)
    
    def analyze_performance(self) -> Dict[str, float]:
        """Analyze performance trends."""
        if len(self.performance_history) < 10:
            return {"status": "insufficient_data"}
        
        recent = self.performance_history[-10:]
        avg_time = sum(m.planning_time for m in recent) / len(recent)
        avg_quality = sum(m.plan_quality for m in recent) / len(recent)
        avg_success = sum(m.success_rate for m in recent) / len(recent)
        
        return {
            "avg_planning_time": avg_time,
            "avg_quality": avg_quality,
            "avg_success_rate": avg_success,
            "bottleneck": "speed" if avg_time > 0.1 else "quality" if avg_quality < 0.8 else "none"
        }
    
    def generate_optimization(self, bottleneck: str) -> CodeOptimization:
        """Generate code optimization based on bottleneck."""
        optimizations = {
            "speed": CodeOptimization(
                optimization_type="caching",
                code_change="Add memoization to frequently called functions",
                expected_improvement=2.0
            ),
            "quality": CodeOptimization(
                optimization_type="heuristic_improvement",
                code_change="Improve cost function with learned weights",
                expected_improvement=1.5
            ),
            "memory": CodeOptimization(
                optimization_type="pruning",
                code_change="Add early pruning of low-quality branches",
                expected_improvement=1.3
            )
        }
        return optimizations.get(bottleneck, optimizations["speed"])
    
    def self_improve(self) -> Dict[str, Any]:
        """Analyze performance and improve own algorithm."""
        analysis = self.analyze_performance()
        
        if analysis.get("status") == "insufficient_data":
            return {"status": "need_more_data", "samples_needed": 10 - len(self.performance_history)}
        
        bottleneck = analysis["bottleneck"]
        
        if bottleneck == "none":
            return {"status": "optimal", "message": "No improvements needed"}
        
        # Generate optimization
        optimization = self.generate_optimization(bottleneck)
        self.optimization_history.append(optimization)
        
        # Apply optimization (simulate code rewriting)
        if optimization.optimization_type == "caching":
            self.planning_speed_multiplier *= optimization.expected_improvement
        elif optimization.optimization_type == "heuristic_improvement":
            self.intelligence_multiplier *= optimization.expected_improvement
        elif optimization.optimization_type == "pruning":
            self.planning_speed_multiplier *= 1.5
            self.intelligence_multiplier *= 1.2
        
        self.current_algorithm_version += 0.1
        
        return {
            "status": "improved",
            "optimization": optimization.optimization_type,
            "speed_multiplier": self.planning_speed_multiplier,
            "intelligence_multiplier": self.intelligence_multiplier,
            "version": self.current_algorithm_version,
            "code_change": optimization.code_change
        }
    
    def get_improvement_stats(self) -> Dict[str, Any]:
        """Get statistics on self-improvement."""
        if not self.optimization_history:
            return {"optimizations": 0, "total_improvement": 1.0}
        
        return {
            "optimizations": len(self.optimization_history),
            "speed_improvement": f"{self.planning_speed_multiplier:.1f}x",
            "intelligence_improvement": f"{self.intelligence_multiplier:.1f}x",
            "algorithm_version": self.current_algorithm_version,
            "optimization_types": [opt.optimization_type for opt in self.optimization_history]
        }
