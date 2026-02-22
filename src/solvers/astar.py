"""
Author: Priyansh Nayak
Description: A* solver for the Maze
    supports both Manhattan and Euclidean distance
"""

import time
import heapq


def manhattan(a, b) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def astar_solver(maze, heuristic):
    start_time = time.perf_counter()
    start = maze.start
    goal = maze.goal
    # tie breaker avoids comparing cells when f is equal
    open_set = []
    tie_breaker = 0
    # g = best-known cost from start to cell
    g = {start: 0}
    # parent pointers for path reconstruction
    parent = {}
    # closed_set set tracks nodes we've fully expanded
    closed_set = set()
    # Metrics
    nodes_expanded = 0
    memory_usage = 1

    start_f = heuristic(start, goal)
    heapq.heappush(open_set, (start_f, tie_breaker, start))

    while open_set:
        _, _, current = heapq.heappop(open_set)
        # If we already expanded it via a better route, skip
        if current in closed_set:
            continue
        closed_set.add(current)
        nodes_expanded += 1
        if current == goal:
            break
        for nbr in maze.neighbors(current):
            tentative_g = g[current] + 1  # each move costs 1

            # If this route to nbr is better, record it
            if nbr not in g or tentative_g < g[nbr]:
                g[nbr] = tentative_g
                parent[nbr] = current

                tie_breaker += 1
                f = tentative_g + heuristic(nbr, goal)
                heapq.heappush(open_set, (f, tie_breaker, nbr))

        memory_usage = max(memory_usage, len(open_set))

    # Reconstruct path
    path = []
    if goal in closed_set:
        cur = goal
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        path.append(start)
        path.reverse()

    runtime = time.perf_counter() - start_time

    return {
        "path": path,
        "moves": max(0, len(path) - 1),
        "nodes_expanded": nodes_expanded,
        "runtime": runtime,
        "memory": memory_usage,
    }