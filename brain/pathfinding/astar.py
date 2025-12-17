"""A* pathfinding algorithm - optimal path with heuristic."""

import heapq
from typing import Any


class AStar:
    """A* algorithm for optimal pathfinding."""

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find shortest path using A* algorithm."""
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

        # Priority queue: (f_score, counter, position)
        counter = 0
        open_set = [(heuristic(start), counter, start)]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {start: 0}
        f_score: dict[tuple[int, int], float] = {start: heuristic(start)}

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return {
                    "success": True,
                    "path": path,
                    "length": len(path),
                    "cost": g_score[goal],
                    "algorithm": "A*",
                }

            for neighbor in get_neighbors(current):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor)

                    counter += 1
                    heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))

        return {"success": False, "message": "No path found", "algorithm": "A*"}

    def _reconstruct_path(
        self, came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
