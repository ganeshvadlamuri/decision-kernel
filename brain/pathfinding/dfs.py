"""Depth-First Search - explores deeply before backtracking."""

from typing import Any


class DFS:
    """DFS algorithm for path finding."""

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: list[list[int]],
    ) -> dict[str, Any]:
        """Find path using DFS."""
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

        visited = set()
        path: list[tuple[int, int]] = []

        def dfs_recursive(current: tuple[int, int]) -> bool:
            """Recursive DFS."""
            if current == goal:
                path.append(current)
                return True

            visited.add(current)
            path.append(current)

            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    if dfs_recursive(neighbor):
                        return True

            path.pop()
            return False

        if dfs_recursive(start):
            return {
                "success": True,
                "path": path,
                "length": len(path),
                "cost": len(path) - 1,
                "algorithm": "DFS",
            }

        return {"success": False, "message": "No path found", "algorithm": "DFS"}
