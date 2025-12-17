"""Breadth-First Search - unweighted shortest path."""

from collections import deque
from typing import Any


class BFS:
    """BFS algorithm for unweighted shortest path."""

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find shortest path using BFS."""
        rows, cols = len(grid), len(grid[0])

        def get_neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
            """Get valid neighbors."""
            r, c = pos
            neighbors = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    neighbors.append((nr, nc))
            return neighbors

        queue: deque[tuple[int, int]] = deque([start])
        visited = {start}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}

        while queue:
            current = queue.popleft()

            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return {
                    "success": True,
                    "path": path,
                    "length": len(path),
                    "cost": len(path) - 1,
                    "algorithm": "BFS",
                }

            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return {"success": False, "message": "No path found", "algorithm": "BFS"}

    def _reconstruct_path(
        self, came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
