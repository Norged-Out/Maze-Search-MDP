from src.maze.generator import generate_maze
from src.maze.render import render_ascii

m = generate_maze(10, 10, seed=1)
render_ascii(m)