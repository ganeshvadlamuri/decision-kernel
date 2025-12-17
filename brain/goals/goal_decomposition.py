"""Goal decomposition - Break complex goals into subgoals."""


class GoalDecomposer:
    """Break complex goals into subgoals."""

    def __init__(self) -> None:
        self.decomposition_rules: dict[str, list[str]] = {
            "clean_house": ["vacuum_floors", "dust_surfaces", "organize_items"],
            "make_dinner": ["get_ingredients", "prepare_food", "cook_food", "serve_food"],
            "do_laundry": ["collect_clothes", "wash_clothes", "dry_clothes", "fold_clothes"],
        }

    def decompose(self, goal: str) -> list[str]:
        """Decompose goal into subgoals."""
        if goal in self.decomposition_rules:
            return self.decomposition_rules[goal]
        return [goal]  # Atomic goal

    def is_atomic(self, goal: str) -> bool:
        """Check if goal is atomic (cannot be decomposed)."""
        return goal not in self.decomposition_rules
