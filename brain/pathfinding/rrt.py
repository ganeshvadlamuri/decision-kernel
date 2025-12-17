"""RRT (Rapidly-exploring Random Tree) - for complex spaces."""

import random
from typing import Any


class RRT:
    """RRT algorithm for path planning in complex spaces."""

    def __init__(self, max_iterations: int = 1000, step_size: float = 1.0) -> None:
        self.max_iterations = max_iterations
        self.step_size = step_size

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find path using RRT algorithm."""
        rows, cols = len(grid), len(grid[0])

        # Tree nodes: position -> parent position
        tree: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        def distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
            """Euclidean distance."""
            return float(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)

        def nearest_node(point: tuple[int, int]) -> tuple[int, int]:
            """Find nearest node in tree."""
            nodes = list(tree.keys())
            return min(nodes, key=lambda n: distance(n, point))

        def steer(
            from_node: tuple[int, int], to_point: tuple[int, int]
        ) -> tuple[int, int]:
            """Steer from node toward point."""
            dist = distance(from_node, to_point)
            if dist <= self.step_size:
                return to_point

            # Move step_size toward to_point
            ratio = self.step_size / dist
            new_x = int(from_node[0] + ratio * (to_point[0] - from_node[0]))
            new_y = int(from_node[1] + ratio * (to_point[1] - from_node[1]))
            return (new_x, new_y)

        def is_collision_free(point: tuple[int, int]) -> bool:
            """Check if point is valid."""
            x, y = point
            return 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0

        # RRT main loop
        for _ in range(self.max_iterations):
            # Sample random point (bias toward goal 10% of time)
            if random.random() < 0.1:
                random_point = goal
            else:
                random_point = (random.randint(0, rows - 1), random.randint(0, cols - 1))

            # Find nearest node
            nearest = nearest_node(random_point)

            # Steer toward random point
            new_node = steer(nearest, random_point)

            # Check collision
            if is_collision_free(new_node):
                tree[new_node] = nearest

                # Check if reached goal
                if distance(new_node, goal) <= self.step_size:
                    tree[goal] = new_node
                    path = self._reconstruct_path(tree, goal)
                    return {
                        "success": True,
                        "path": path,
                        "length": len(path),
                        "cost": self._path_cost(path),
                        "algorithm": "RRT",
                    }

        return {"success": False, "message": "Max iterations reached", "algorithm": "RRT"}

    def _reconstruct_path(
        self, tree: dict[tuple[int, int], tuple[int, int] | None], goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Reconstruct path from tree."""
        path = [goal]
        current = goal
        visited = {goal}
        while tree.get(current) is not None:
            parent = tree[current]
            if parent in visited:  # Prevent infinite loop
                break
            visited.add(parent)  # type: ignore
            current = parent  # type: ignore
            path.append(current)
        return list(reversed(path))

    def _path_cost(self, path: list[tuple[int, int]]) -> float:
        """Calculate path cost."""
        cost = 0.0
        for i in range(len(path) - 1):
            cost += ((path[i][0] - path[i + 1][0]) ** 2 + (path[i][1] - path[i + 1][1]) ** 2) ** 0.5
        return cost
