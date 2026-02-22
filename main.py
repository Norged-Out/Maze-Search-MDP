from src.maze.generator import generate_maze
from src.maze.render import render_ascii, render_matplotlib
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver
from src.solvers.astar import astar_solver, manhattan, euclidean
from src.solvers.value_iter import value_iteration
from src.solvers.policy_iter import policy_iteration
from src.solvers.utils import extract_path

print("Generating Maze...")
maze = generate_maze(20, 20, seed=200, openness=0.1)
render_ascii(maze)
render_matplotlib(maze)


# ---- DFS ----
dfs_result = dfs_solver(maze)

print("\nDFS results:")
print("Moves:", dfs_result["moves"])
print("Nodes expanded:", dfs_result["nodes_expanded"])
print("Runtime:", dfs_result["runtime"])
print("Memory:", dfs_result["memory"])

render_ascii(maze, path=dfs_result["path"])
render_matplotlib(maze, explored=dfs_result["explored"], path=dfs_result["path"], title="DFS")


# ---- BFS ----
bfs_result = bfs_solver(maze)

print("\nBFS results:")
print("Moves:", bfs_result["moves"])
print("Nodes expanded:", bfs_result["nodes_expanded"])
print("Runtime:", bfs_result["runtime"])
print("Memory:", bfs_result["memory"])

render_ascii(maze, path=bfs_result["path"])
render_matplotlib(maze, explored=bfs_result["explored"], path=bfs_result["path"], title="BFS")


# ---- A* Manhattan ----
astar_m = astar_solver(maze, heuristic=manhattan)

print("\nA* Manhattan results:")
print("Moves:", astar_m["moves"])
print("Nodes expanded:", astar_m["nodes_expanded"])
print("Runtime:", astar_m["runtime"])
print("Memory:", astar_m["memory"])

render_ascii(maze, path=astar_m["path"])
render_matplotlib(maze, explored=astar_m["explored"], path=astar_m["path"], title="Manhattan")


# ---- A* Euclidean ----
astar_e = astar_solver(maze, heuristic=euclidean)

print("\nA* Euclidean results:")
print("Moves:", astar_e["moves"])
print("Nodes expanded:", astar_e["nodes_expanded"])
print("Runtime:", astar_e["runtime"])
print("Memory:", astar_e["memory"])

render_ascii(maze, path=astar_e["path"])
render_matplotlib(maze, explored=astar_e["explored"], path=astar_e["path"], title="Euclid")


# ---- Value Iteration ----
g = 0.9
vi_result = value_iteration(maze, gamma=g)
vi_path = extract_path(vi_result["policy"], maze.start, maze.goal)

print(f"\nValue Iteration Results (Gamma = {g}):")
print("Moves:", max(0, len(vi_path) - 1))
print("Iterations:", vi_result["iterations"])
print("State updates:", vi_result["state_updates"])
print("Runtime:", vi_result["runtime"])
print("Final delta:", vi_result["delta"])

render_ascii(maze, path=vi_path)
render_matplotlib(maze, explored=None, path=vi_path, title=f"Value Iteration (Gamma = {g})")


# ---- Policy Iteration ----

pi_result = policy_iteration(maze, gamma=g)
pi_path = extract_path(pi_result["policy"], maze.start, maze.goal)

print(f"\nPolicy Iteration Results (Gamma = {g}):")
print("Moves:", max(0, len(pi_path) - 1))
print("Policy iterations:", pi_result["policy_iterations"])
print("Evaluation iterations:", pi_result["evaluation_iterations"])
print("State updates:", pi_result["state_updates"])
print("Runtime:", pi_result["runtime"])
print("Memory:", pi_result["memory"])

render_ascii(maze, path=pi_path)
render_matplotlib(maze, explored=None, path=pi_path, title=f"Policy Iteration (Gamma = {g})")