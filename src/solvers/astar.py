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
    open_set = [] # f = g + h
    tie_breaker = 0 # avoids comparing cells when f is equal
    g = {start: 0} # best-known cost from start to cell
    parent = {} # for path reconstruction
    closed_set = set() # tracks nodes fully expanded
    # metrics
    nodes_expanded = 0
    memory_usage = 1
    explored_order = [] # for pygame

    start_f = heuristic(start, goal)
    heapq.heappush(open_set, (start_f, tie_breaker, start))

    while open_set:
        _, _, current = heapq.heappop(open_set)
        # if already expanded it via a better route, skip
        if current in closed_set:
            continue
        closed_set.add(current)
        nodes_expanded += 1
        explored_order.append(current)
        if current == goal:
            break
        for nbr in maze.neighbors(current):
            tentative_g = g[current] + 1  # each move costs 1
            # if this route is better, record it
            if nbr not in g or tentative_g < g[nbr]:
                g[nbr] = tentative_g
                parent[nbr] = current
                tie_breaker += 1
                f = tentative_g + heuristic(nbr, goal)
                heapq.heappush(open_set, (f, tie_breaker, nbr))

        memory_usage = max(memory_usage, len(open_set))

    # reconstruct path
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
        "explored": closed_set,
        "explored_order": explored_order
    }