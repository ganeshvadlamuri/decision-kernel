"""Greedy Best-First Search - fast but not optimal."""

import heapq
from typing import Any


class GreedyBestFirst:
    """Greedy Best-First Search algorithm."""

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find path using Greedy Best-First Search."""
        rows, cols = len(grid), len(grid[0])

        def heuristic(pos: tuple[int, int]) -> float:
            """Manhattan distance heuristic."""
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        def get_neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
            """Get valid neighbors."""
            r, c = pos
            neighbors = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    neighbors.append((nr, nc))
            return neighbors

        # Priority queue: (heuristic, counter, position)
        counter = 0
        open_set = [(heuristic(start), counter, start)]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        visited = set()

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return {
                    "success": True,
                    "path": path,
                    "length": len(path),
                    "cost": len(path) - 1,
                    "algorithm": "Greedy Best-First",
                }

            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                        counter += 1
                        heapq.heappush(open_set, (heuristic(neighbor), counter, neighbor))

        return {
            "success": False,
            "message": "No path found",
            "algorithm": "Greedy Best-First",
        }

    def _reconstruct_path(
        self, came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
