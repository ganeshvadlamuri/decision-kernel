"""Skill Synthesis - Combines existing skills to create new ones automatically."""
from dataclasses import dataclass
from typing import List, Dict, Any, Set
from brain.planner.actions import Action


@dataclass
class Skill:
    name: str
    actions: List[Action]
    preconditions: List[str]
    effects: List[str]
    complexity: int


@dataclass
class SynthesizedSkill:
    name: str
    parent_skills: List[str]
    actions: List[Action]
    novelty_score: float
    usefulness_score: float


class SkillSynthesizer:
    def __init__(self):
        self.known_skills: Dict[str, Skill] = {}
        self.synthesized_skills: Dict[str, SynthesizedSkill] = {}
        self._initialize_base_skills()
    
    def _initialize_base_skills(self):
        """Initialize base skills library."""
        self.known_skills = {
            "pour_liquid": Skill(
                name="pour_liquid",
                actions=[
                    Action(action_type="grasp", target="container", parameters={}),
                    Action(action_type="tilt", target="container", parameters={"angle": 45}),
                    Action(action_type="pour", parameters={"speed": "medium"}),
                    Action(action_type="upright", target="container", parameters={})
                ],
                preconditions=["container_available", "liquid_in_container"],
                effects=["liquid_poured"],
                complexity=2
            ),
            "navigate": Skill(
                name="navigate",
                actions=[
                    Action(action_type="plan_path", location="target", parameters={}),
                    Action(action_type="navigate", location="target", parameters={}),
                    Action(action_type="verify_arrival", parameters={})
                ],
                preconditions=["path_exists"],
                effects=["at_target_location"],
                complexity=1
            ),
            "detect_spill": Skill(
                name="detect_spill",
                actions=[
                    Action(action_type="scan_floor", parameters={"range": 2.0}),
                    Action(action_type="analyze_wetness", parameters={}),
                    Action(action_type="mark_spill_location", parameters={})
                ],
                preconditions=["sensors_active"],
                effects=["spill_detected"],
                complexity=1
            ),
            "grasp_object": Skill(
                name="grasp_object",
                actions=[
                    Action(action_type="approach", target="object", parameters={}),
                    Action(action_type="align_gripper", parameters={}),
                    Action(action_type="grasp", target="object", parameters={}),
                    Action(action_type="verify_grasp", parameters={})
                ],
                preconditions=["object_visible"],
                effects=["object_grasped"],
                complexity=2
            ),
            "avoid_obstacle": Skill(
                name="avoid_obstacle",
                actions=[
                    Action(action_type="detect_obstacle", parameters={}),
                    Action(action_type="calculate_detour", parameters={}),
                    Action(action_type="navigate", location="detour", parameters={})
                ],
                preconditions=["obstacle_detected"],
                effects=["obstacle_avoided"],
                complexity=1
            )
        }
    
    def combine(self, skill_names: List[str], goal: str = None) -> SynthesizedSkill:
        """Combine existing skills to create a new one."""
        # Validate skills exist
        skills = [self.known_skills[name] for name in skill_names if name in self.known_skills]
        
        if len(skills) < 2:
            raise ValueError("Need at least 2 skills to combine")
        
        # Generate new skill name
        new_name = self._generate_skill_name(skill_names, goal)
        
        # Synthesize actions
        synthesized_actions = self._synthesize_actions(skills)
        
        # Calculate scores
        novelty = self._calculate_novelty(new_name, skills)
        usefulness = self._calculate_usefulness(skills)
        
        synthesized = SynthesizedSkill(
            name=new_name,
            parent_skills=skill_names,
            actions=synthesized_actions,
            novelty_score=novelty,
            usefulness_score=usefulness
        )
        
        self.synthesized_skills[new_name] = synthesized
        return synthesized
    
    def _generate_skill_name(self, skill_names: List[str], goal: str = None) -> str:
        """Generate name for synthesized skill."""
        if goal:
            return goal
        
        # Intelligent naming based on combination
        if "pour_liquid" in skill_names and "navigate" in skill_names:
            if "detect_spill" in skill_names:
                return "serve_drink_carefully"
            return "deliver_liquid"
        
        if "grasp_object" in skill_names and "navigate" in skill_names:
            if "avoid_obstacle" in skill_names:
                return "fetch_and_deliver_safely"
            return "fetch_and_deliver"
        
        # Default: combine names
        return "_and_".join(skill_names[:2])
    
    def _synthesize_actions(self, skills: List[Skill]) -> List[Action]:
        """Intelligently combine actions from multiple skills."""
        synthesized = []
        
        # Interleave actions intelligently
        if len(skills) == 2:
            skill1, skill2 = skills
            
            # Pattern: navigate + action
            if skill2.name == "navigate":
                synthesized.extend(skill2.actions)
                synthesized.extend(skill1.actions)
            # Pattern: action + safety check
            elif "detect" in skill2.name or "avoid" in skill2.name:
                for action in skill1.actions:
                    synthesized.append(action)
                    if action.action_type in ["pour", "navigate", "grasp"]:
                        synthesized.extend(skill2.actions)
            else:
                synthesized.extend(skill1.actions)
                synthesized.extend(skill2.actions)
        else:
            # Multiple skills: layer them
            for skill in skills:
                synthesized.extend(skill.actions)
        
        return synthesized
    
    def _calculate_novelty(self, name: str, skills: List[Skill]) -> float:
        """Calculate how novel this combination is."""
        if name in self.synthesized_skills:
            return 0.0
        
        # Check if similar combinations exist
        parent_set = set(s.name for s in skills)
        for existing in self.synthesized_skills.values():
            existing_set = set(existing.parent_skills)
            overlap = len(parent_set & existing_set) / len(parent_set | existing_set)
            if overlap > 0.5:
                return 0.3
        
        return 0.9
    
    def _calculate_usefulness(self, skills: List[Skill]) -> float:
        """Calculate how useful this combination is."""
        # More complex skills = more useful
        total_complexity = sum(s.complexity for s in skills)
        
        # Complementary effects = more useful
        all_effects = set()
        for skill in skills:
            all_effects.update(skill.effects)
        
        usefulness = min(1.0, (total_complexity * 0.2) + (len(all_effects) * 0.15))
        return usefulness
    
    def auto_discover_combinations(self, max_combinations: int = 5) -> List[SynthesizedSkill]:
        """Automatically discover useful skill combinations."""
        discovered = []
        skill_list = list(self.known_skills.keys())
        
        # Try promising combinations
        promising_pairs = [
            (["pour_liquid", "navigate"], "deliver_liquid"),
            (["pour_liquid", "navigate", "detect_spill"], "serve_drink_carefully"),
            (["grasp_object", "navigate"], "fetch_and_deliver"),
            (["navigate", "avoid_obstacle"], "navigate_safely"),
            (["grasp_object", "detect_spill"], "careful_handling")
        ]
        
        for skills, goal in promising_pairs[:max_combinations]:
            if all(s in self.known_skills for s in skills):
                try:
                    synthesized = self.combine(skills, goal)
                    discovered.append(synthesized)
                except:
                    pass
        
        return discovered
    
    def get_synthesis_stats(self) -> Dict[str, Any]:
        """Get statistics on skill synthesis."""
        return {
            "base_skills": len(self.known_skills),
            "synthesized_skills": len(self.synthesized_skills),
            "avg_novelty": sum(s.novelty_score for s in self.synthesized_skills.values()) / max(1, len(self.synthesized_skills)),
            "avg_usefulness": sum(s.usefulness_score for s in self.synthesized_skills.values()) / max(1, len(self.synthesized_skills))
        }
