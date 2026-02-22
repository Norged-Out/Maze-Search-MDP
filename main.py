from src.maze.generator import generate_maze
from src.maze.render import render_ascii, render_matplotlib
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver
from src.solvers.astar import astar_solver, manhattan, euclidean

print("Generating Maze...")
m = generate_maze(50, 50, seed=200, openness=0.2)
render_matplotlib(m)

# ---- DFS ----
dfs_result = dfs_solver(m)

print("\nDFS results:")
print("Moves:", dfs_result["moves"])
print("Nodes expanded:", dfs_result["nodes_expanded"])
print("Runtime:", dfs_result["runtime"])
print("Memory:", dfs_result["memory"])

render_matplotlib(m, explored=dfs_result["explored"], path=dfs_result["path"], title="DFS")


# ---- BFS ----
bfs_result = bfs_solver(m)

print("\nBFS results:")
print("Moves:", bfs_result["moves"])
print("Nodes expanded:", bfs_result["nodes_expanded"])
print("Runtime:", bfs_result["runtime"])
print("Memory:", bfs_result["memory"])

render_matplotlib(m, explored=bfs_result["explored"], path=bfs_result["path"], title="BFS")


# ---- A* Manhattan ----
astar_m = astar_solver(m, heuristic=manhattan)

print("\nA* Manhattan results:")
print("Moves:", astar_m["moves"])
print("Nodes expanded:", astar_m["nodes_expanded"])
print("Runtime:", astar_m["runtime"])
print("Memory:", astar_m["memory"])

render_matplotlib(m, explored=astar_m["explored"], path=astar_m["path"], title="Manhattan")


# ---- A* Euclidean ----
astar_e = astar_solver(m, heuristic=euclidean)

print("\nA* Euclidean results:")
print("Moves:", astar_e["moves"])
print("Nodes expanded:", astar_e["nodes_expanded"])
print("Runtime:", astar_e["runtime"])
print("Memory:", astar_e["memory"])

render_matplotlib(m, explored=astar_e["explored"], path=astar_e["path"], title="Euclid")