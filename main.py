from src.maze.generator import generate_maze
from src.maze.render import render_ascii
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver


m = generate_maze(10, 10, seed=2)

print("\nMaze:")
render_ascii(m)

# ---- DFS ----
dfs_result = dfs_solver(m)

print("\nDFS results:")
print("Moves:", dfs_result["moves"])
print("Nodes expanded:", dfs_result["nodes_expanded"])
print("Runtime:", dfs_result["runtime"])
print("Memory:", dfs_result["memory"])

render_ascii(m, dfs_result["path"])


# ---- BFS ----
bfs_result = bfs_solver(m)

print("\nBFS results:")
print("Moves:", bfs_result["moves"])
print("Nodes expanded:", bfs_result["nodes_expanded"])
print("Runtime:", bfs_result["runtime"])
print("Memory:", bfs_result["memory"])

render_ascii(m, bfs_result["path"])