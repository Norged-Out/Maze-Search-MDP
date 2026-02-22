"""
Author: Priyansh Nayak
Description: ASCII rendering utilities for visualising the maze
"""


def render_ascii(maze, path=None) -> None:
    """
    Render the maze in ASCII form.

    Symbols:
    S = start
    G = goal
    . = solution path
    _ = bottom walls
    | = vertical walls
    spaces for open corridors
    """
    h, w = maze.height, maze.width
    path = set(path or [])
    # draw top border
    print(" " + "_" * (2 * w - 1))
    for r in range(h):
        # line with vertical walls + symbols
        line1 = "|"
        # line with bottom walls
        line2 = "|"
        for c in range(w):
            cell = (r, c)
            # choose interior symbol
            if cell == maze.start:
                symbol = "S"
            elif cell == maze.goal:
                symbol = "G"
            elif cell in path:
                symbol = "."
            else:
                symbol = " "

            # upper line (cell interior + right wall)
            line1 += symbol

            if maze.has_wall(cell, "E"):
                line1 += "|"
            else:
                line1 += " "

            # lower line (bottom wall + corner)
            if maze.has_wall(cell, "S"):
                line2 += "_"
            else:
                line2 += " "

            if maze.has_wall(cell, "E"):
                line2 += "|"
            else:
                line2 += " "

        print(line1)
        print(line2)