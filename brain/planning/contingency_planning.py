"""Contingency planning - Backup plans for failures."""



class ContingencyPlanner:
    """Backup plans for failures."""

    def generate_contingencies(self, primary_plan: list[str]) -> dict[str, list[str]]:
        """Generate backup plans for each action."""
        contingencies = {}

        for action in primary_plan:
            contingencies[action] = self._get_alternatives(action)

        return contingencies

    def _get_alternatives(self, action: str) -> list[str]:
        """Get alternative actions."""
        alternatives = {
            "navigate": ["find_alternate_route", "wait_for_clearance"],
            "grasp": ["try_different_grip", "use_tool"],
            "search": ["ask_human", "check_common_locations"],
        }

        for key, alts in alternatives.items():
            if key in action.lower():
                return alts

        return ["retry", "ask_for_help"]
