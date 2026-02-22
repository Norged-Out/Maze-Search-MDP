"""
Author: Priyansh Nayak
Description: BFS Solver for my Maze
"""

import time
from collections import deque


def bfs_solver(maze):
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    queue = deque([start])
    visited = {start}
    parent = {}

    nodes_expanded = 0
    memory_usage = 1

    while queue:
        current = queue.popleft()  # FIFO
        nodes_expanded += 1

        if current == goal:
            break

        for nbr in maze.neighbors(current):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = current
                queue.append(nbr)

        memory_usage = max(memory_usage, len(queue))

    # reconstruct path
    path = []
    if goal in visited:
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