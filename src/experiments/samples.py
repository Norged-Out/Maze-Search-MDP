"""
Author: Priyansh Nayak
Description: Sample runs of the maze generation
"""
from src.maze.generator import generate_maze
from src.maze.render import render_matplotlib
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver
from src.solvers.astar import astar_solver, manhattan, euclidean
from src.solvers.value_iter import value_iteration
from src.solvers.policy_iter import policy_iteration
from src.solvers.utils import extract_path
import os

def generate_samples():
    # --------------------------------------------------
    # 1. Unsolved Maze
    # --------------------------------------------------
    seed = 49620

    maze = generate_maze(30, 30, seed=seed, openness=0)
    render_matplotlib(maze, title="Unsolved Maze (30x30)")


    # --------------------------------------------------
    # 2. Same Maze – All Solvers
    # --------------------------------------------------

    # DFS
    res = dfs_solver(maze)
    path, explored = res["path"], res["explored"]
    render_matplotlib(maze, path=path, explored=explored,
                    title="DFS Solution (30x30)")

    # BFS
    res = bfs_solver(maze)
    path, explored = res["path"], res["explored"]
    render_matplotlib(maze, path=path, explored=explored,
                    title="BFS Solution (30x30)")

    # A* Manhattan
    res = astar_solver(maze, manhattan)
    path, explored = res["path"], res["explored"]
    render_matplotlib(maze, path=path, explored=explored,
                    title="Astar Manhattan (30x30)")

    # A* Euclidean
    res = astar_solver(maze, euclidean)
    path, explored = res["path"], res["explored"]
    render_matplotlib(maze, path=path, explored=explored,
                    title="Astar Euclidean (30x30)")

    # Value Iteration
    res = value_iteration(maze)
    policy = res["policy"]
    path = extract_path(policy, maze.start, maze.goal)
    render_matplotlib(maze, path=path, policy=policy, title="Value Iteration Policy (30x30)")

    # Policy Iteration
    res = policy_iteration(maze)
    policy = res["policy"]
    path = extract_path(policy, maze.start, maze.goal)
    render_matplotlib(maze, path=path, policy=policy, title="Policy Iteration Policy (30x30)")


    # --------------------------------------------------
    # 3. Size Comparison (A* Manhattan)
    # --------------------------------------------------

    for size in [10, 30, 50]:
        maze = generate_maze(size, size, seed=seed, openness=0)

        res = astar_solver(maze, manhattan)  # or heuristic=manhattan if required
        path, explored = res["path"], res["explored"]

        render_matplotlib(
            maze,
            path=path,
            explored=explored,
            title=f"Astar Manhattan Size {size}x{size})"
        )


    # --------------------------------------------------
    # 4. Openness Comparison (A* Manhattan)
    # --------------------------------------------------

    for openness in [0.0, 0.1, 0.2, 0.3]:
        maze = generate_maze(30, 30, seed=seed, openness=openness)

        res = astar_solver(maze, manhattan)  # or heuristic=manhattan if needed
        path, explored = res["path"], res["explored"]

        render_matplotlib(
            maze,
            path=path,
            explored=explored,
            title=f"Astar Manhattan Openness {openness}"
        )


    print("Sample renders saved in 'samples/' directory.")