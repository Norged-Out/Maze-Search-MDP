"""
Author: Priyansh Nayak
Description: ASCII rendering utilities for visualising the maze
"""

def render_ascii(maze) -> None:
    """
    Render the maze in ASCII form.

    Uses:
    '_' for bottom walls
    '|' for vertical walls
    spaces for open corridors
    """

    h, w = maze.height, maze.width

    # Draw top border
    print(" " + "_" * (w * 2 - 1))

    # Draw each row of the maze
    for r in range(h):
        line = "|"

        for c in range(w):
            # Bottom wall (South)
            if maze.has_wall((r, c), "S"):
                line += "_"
            else:
                line += " "

            # Right wall (East)
            if maze.has_wall((r, c), "E"):
                line += "|"
            else:
                line += " "

        print(line)