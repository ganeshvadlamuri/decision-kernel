"""Dijkstra's algorithm - optimal path without heuristic."""

import heapq
from typing import Any


class Dijkstra:
    """Dijkstra's algorithm for shortest path."""

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find shortest path using Dijkstra's algorithm."""
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

        # Priority queue: (distance, counter, position)
        counter = 0
        pq = [(0, counter, start)]
        distances: dict[tuple[int, int], float] = {start: 0}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}

        while pq:
            dist, _, current = heapq.heappop(pq)

            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return {
                    "success": True,
                    "path": path,
                    "length": len(path),
                    "cost": distances[goal],
                    "algorithm": "Dijkstra",
                }

            if dist > distances.get(current, float("inf")):
                continue

            for neighbor in get_neighbors(current):
                new_dist = dist + 1

                if new_dist < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current
                    counter += 1
                    heapq.heappush(pq, (new_dist, counter, neighbor))

        return {"success": False, "message": "No path found", "algorithm": "Dijkstra"}

    def _reconstruct_path(
        self, came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
