"""Demo of all pathfinding algorithms."""

from brain.pathfinding import AStar, BFS, DFS, Dijkstra, GreedyBestFirst, RRT


def create_test_grid() -> list[list[int]]:
    """Create test grid (0=free, 1=obstacle)."""
    return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]


def visualize_path(grid: list[list[int]], path: list[tuple[int, int]]) -> None:
    """Visualize path on grid."""
    path_set = set(path)
    for i, row in enumerate(grid):
        line = ""
        for j, cell in enumerate(row):
            if (i, j) == path[0]:
                line += "S "  # Start
            elif (i, j) == path[-1]:
                line += "G "  # Goal
            elif (i, j) in path_set:
                line += "* "  # Path
            elif cell == 1:
                line += "# "  # Obstacle
            else:
                line += ". "  # Free
        print(line)


def demo_astar() -> None:
    """Demo A* algorithm."""
    print("\n=== 1. A* ALGORITHM ===")
    print("Optimal path with heuristic (Manhattan distance)\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    astar = AStar()
    result = astar.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']}")
        print("\nPath visualization:")
        visualize_path(grid, result["path"])


def demo_dijkstra() -> None:
    """Demo Dijkstra's algorithm."""
    print("\n=== 2. DIJKSTRA'S ALGORITHM ===")
    print("Optimal path without heuristic\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    dijkstra = Dijkstra()
    result = dijkstra.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']}")


def demo_bfs() -> None:
    """Demo BFS algorithm."""
    print("\n=== 3. BREADTH-FIRST SEARCH (BFS) ===")
    print("Unweighted shortest path\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    bfs = BFS()
    result = bfs.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']}")


def demo_dfs() -> None:
    """Demo DFS algorithm."""
    print("\n=== 4. DEPTH-FIRST SEARCH (DFS) ===")
    print("Explores deeply before backtracking\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    dfs = DFS()
    result = dfs.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']}")
        print("Note: DFS path is usually not optimal")


def demo_greedy() -> None:
    """Demo Greedy Best-First Search."""
    print("\n=== 5. GREEDY BEST-FIRST SEARCH ===")
    print("Fast but not always optimal\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    greedy = GreedyBestFirst()
    result = greedy.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']}")


def demo_rrt() -> None:
    """Demo RRT algorithm."""
    print("\n=== 6. RRT (RAPIDLY-EXPLORING RANDOM TREE) ===")
    print("For complex/high-dimensional spaces\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    rrt = RRT(max_iterations=500, step_size=1.5)
    result = rrt.find_path(start, goal, grid)

    print(f"Start: {start}, Goal: {goal}")
    print(f"Success: {result['success']}")
    if result["success"]:
        print(f"Path length: {result['length']} steps")
        print(f"Path cost: {result['cost']:.2f}")
        print("Note: RRT path is probabilistically complete")


def compare_algorithms() -> None:
    """Compare all algorithms."""
    print("\n=== ALGORITHM COMPARISON ===\n")

    grid = create_test_grid()
    start = (0, 0)
    goal = (9, 9)

    algorithms = [
        ("A*", AStar()),
        ("Dijkstra", Dijkstra()),
        ("BFS", BFS()),
        ("DFS", DFS()),
        ("Greedy", GreedyBestFirst()),
        ("RRT", RRT(max_iterations=500)),
    ]

    print(f"{'Algorithm':<15} {'Success':<10} {'Length':<10} {'Cost':<10}")
    print("-" * 50)

    for name, algo in algorithms:
        result = algo.find_path(start, goal, grid)
        success = "Yes" if result["success"] else "No"
        length = result.get("length", "-")
        cost = result.get("cost", "-")
        if isinstance(cost, float):
            cost = f"{cost:.2f}"
        print(f"{name:<15} {success:<10} {str(length):<10} {str(cost):<10}")


def main() -> None:
    """Run all pathfinding demos."""
    print("=" * 60)
    print("PATHFINDING ALGORITHMS DEMO")
    print("6 Algorithms for Motion Planning")
    print("=" * 60)

    demo_astar()
    demo_dijkstra()
    demo_bfs()
    demo_dfs()
    demo_greedy()
    demo_rrt()
    compare_algorithms()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Total: 6 pathfinding algorithms")
    print("\nAlgorithm characteristics:")
    print("  A*: Optimal, fast with good heuristic")
    print("  Dijkstra: Optimal, no heuristic needed")
    print("  BFS: Optimal for unweighted graphs")
    print("  DFS: Memory efficient, not optimal")
    print("  Greedy: Fast, not always optimal")
    print("  RRT: Good for complex/high-dimensional spaces")
    print("\nUse in adapters for low-level motion planning!")


if __name__ == "__main__":
    main()
