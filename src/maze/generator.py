"""
Author: Priyansh Nayak
Description: Generators a solvable maze
    using Recursive Backtracking
"""
import random
from src.maze.maze import Maze, DIRS, DELTAS


def generate_maze(height: int, width: int, seed: int | None = None, openness: float = 0.0) -> Maze:
    # seed for reproducibility 
    if seed is not None:
        random.seed(seed)

    maze = Maze(height, width)

    visited = set()
    stack = [(0, 0)]
    visited.add((0, 0))

    # explore maze with RBT
    while stack:
        r, c = stack[-1] # current cell

        # collect unvisited neighbours with direction info
        options = []
        for d in DIRS:
            dr, dc = DELTAS[d]
            nr, nc = r + dr, c + dc
            # valid neighbour and unvisited
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in visited:
                options.append((d, (nr, nc)))
        # carve a passage
        if options:
            direction, nxt = random.choice(options)
            # remove the wall between current cell and chosen neighbour
            maze.remove_wall((r, c), direction)
            # mark neighbour visited and continue
            visited.add(nxt)
            stack.append(nxt)
        else:
            stack.pop() # dead end

    # add extra random connections to introduce loops
    if openness > 0:
        possible_walls = []
        # collect all removable interior walls
        for r in range(height):
            for c in range(width):
                for d in DIRS:
                    dr, dc = DELTAS[d]
                    nr, nc = r + dr, c + dc
                    # ensure neighbour exists
                    if 0 <= nr < height and 0 <= nc < width:
                        # only consider valid walls
                        if maze.has_wall((r, c), d):
                            possible_walls.append(((r, c), d))
        # random distribution of open walls 
        random.shuffle(possible_walls)
        loops_to_add = int(len(possible_walls) * openness)
        # add the alternate paths
        for (cell, d) in possible_walls[:loops_to_add]:
            if maze.has_wall(cell, d):
                maze.remove_wall(cell, d)

    return maze