"""
Author: Priyansh Nayak
Description: Runs experiments across maze sizes / seeds / openness and collects metrics
"""

from src.maze.generator import generate_maze
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver
from src.solvers.astar import astar_solver, manhattan, euclidean
from src.solvers.value_iter import value_iteration
from src.solvers.policy_iter import policy_iteration
from src.solvers.utils import extract_path


def run_experiments(sizes, seeds, openness_levels, gamma=0.9, epsilon=1e-4):
    # collect raw results (no printing, no rendering)
    results = []

    for n in sizes:
        for openness in openness_levels:
            for seed in seeds:

                maze = generate_maze(n, n, seed=seed, openness=openness)

                # ---- DFS ----
                dfs_res = dfs_solver(maze)
                results.append({
                    "algorithm": "DFS",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": dfs_res["moves"],
                    "runtime": dfs_res["runtime"],
                    "work": dfs_res["nodes_expanded"],
                    "memory": dfs_res["memory"],
                })

                # ---- BFS ----
                bfs_res = bfs_solver(maze)
                results.append({
                    "algorithm": "BFS",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": bfs_res["moves"],
                    "runtime": bfs_res["runtime"],
                    "work": bfs_res["nodes_expanded"],
                    "memory": bfs_res["memory"],
                })

                # ---- A* Manhattan ----
                am_res = astar_solver(maze, heuristic=manhattan)
                results.append({
                    "algorithm": "A*_Manhattan",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": am_res["moves"],
                    "runtime": am_res["runtime"],
                    "work": am_res["nodes_expanded"],
                    "memory": am_res["memory"],
                })

                # ---- A* Euclidean ----
                ae_res = astar_solver(maze, heuristic=euclidean)
                results.append({
                    "algorithm": "A*_Euclidean",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": ae_res["moves"],
                    "runtime": ae_res["runtime"],
                    "work": ae_res["nodes_expanded"],
                    "memory": ae_res["memory"],
                })

                # ---- Value Iteration ----
                vi_res = value_iteration(maze, gamma=gamma, epsilon=epsilon)
                vi_path = extract_path(vi_res["policy"], maze.start, maze.goal)
                results.append({
                    "algorithm": "Value_Iteration",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": max(0, len(vi_path) - 1),
                    "runtime": vi_res["runtime"],
                    "work": vi_res["state_updates"],
                    "memory": vi_res["memory"],
                    "iterations": vi_res["iterations"],
                    "delta": vi_res["delta"],
                })

                # ---- Policy Iteration ----
                pi_res = policy_iteration(maze, gamma=gamma, epsilon=epsilon)
                pi_path = extract_path(pi_res["policy"], maze.start, maze.goal)
                results.append({
                    "algorithm": "Policy_Iteration",
                    "size": n,
                    "seed": seed,
                    "openness": openness,
                    "moves": max(0, len(pi_path) - 1),
                    "runtime": pi_res["runtime"],
                    "work": pi_res["state_updates"],
                    "memory": pi_res["memory"],
                    "policy_iterations": pi_res["policy_iterations"],
                    "evaluation_iterations": pi_res["evaluation_iterations"],
                })

    return results