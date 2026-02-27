"""
Author: Priyansh Nayak
Description: Visualisation Helpers for Maze
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import ListedColormap
import os

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
        line = "|"
        for c in range(w):
            cell = (r, c)
            # choose interior symbol
            if cell in path:
                symbol = "."
            else:
                symbol = " "
            # bottom wall
            if cell in path:
                line += symbol
            elif maze.has_wall(cell, "S"):
                line += "_"
            else:
                line += " "
            # right wall
            if maze.has_wall(cell, "E"):
                line += "|"
            else:
                line += " "
        print(line)


def render_matplotlib(maze, path=None, explored=None, policy=None, title="Maze"):
    """
    Matplotlib renderer (true wall lines).
    """

    h, w = maze.height, maze.width
    path = list(path or [])
    explored = set(explored or [])

    fig, ax = plt.subplots()
    legend_elements = []


    # MDP overlay
    if policy:
        # 0=up, 1=right, 2=down, 3=left, 4=goal/none
        grid = [[4 for _ in range(w)] for _ in range(h)]

        for (r, c), nxt in policy.items():
            if nxt is None:
                continue

            nr, nc = nxt
            dr = nr - r
            dc = nc - c

            if dr == -1:
                grid[r][c] = 0
            elif dc == 1:
                grid[r][c] = 1
            elif dr == 1:
                grid[r][c] = 2
            elif dc == -1:
                grid[r][c] = 3

        # soft academic palette
        cmap = ListedColormap([
            "#8ecae6",  # up
            "#d6d459",  # right
            "#f4a261",  # down
            "#cdb4db",  # left
            "#f0f0f0",  # goal/none
        ])
        legend_elements.extend([
            Patch(facecolor="#8ecae6", label="Policy: Up"),
            Patch(facecolor="#d6d459", label="Policy: Right"),
            Patch(facecolor="#f4a261", label="Policy: Down"),
            Patch(facecolor="#cdb4db", label="Policy: Left"),
        ])

        ax.imshow(
            grid,
            cmap=cmap,
            origin="upper",
            extent=(0, w, h, 0),
            alpha=0.3,
            interpolation="nearest",
        )

    # draw walls
    segments = []  # each segment is [(x1,y1), (x2,y2)]
    for r in range(h):
        for c in range(w):
            cell = (r, c)
            # check all directions
            if maze.has_wall(cell, "N"):
                segments.append([(c, r), (c + 1, r)])
            if maze.has_wall(cell, "S"):
                segments.append([(c, r + 1), (c + 1, r + 1)])
            if maze.has_wall(cell, "W"):
                segments.append([(c, r), (c, r + 1)])
            if maze.has_wall(cell, "E"):
                segments.append([(c + 1, r), (c + 1, r + 1)])

    wall_lines = LineCollection(segments, colors="black", linewidths=1.5)
    ax.add_collection(wall_lines)

    # explored overlay
    if explored:
        patches = [Rectangle((c, r), 1, 1) for (r, c) in explored]
        explored_fill = PatchCollection(patches, edgecolor="none", alpha=0.35)
        ax.add_collection(explored_fill)

    # path overlay
    if path:
        xs = [c + 0.5 for (r, c) in path]
        ys = [r + 0.5 for (r, c) in path]
        ax.plot(xs, ys, color="green", linewidth=2.5)

    # start and goal markers
    sr, sc = maze.start
    gr, gc = maze.goal
    # start
    ax.scatter(
        [sc + 0.5], [sr + 0.5],
        s=35,
        marker="o",
        facecolors="blue",
        edgecolors="black",
        linewidths=0.5,
        zorder=6
    )

    # goal
    ax.scatter(
        [gc + 0.5], [gr + 0.5],
        s=35,
        marker="X",
        facecolors="red",
        edgecolors="black",
        linewidths=0.5,
        zorder=6
    )

    # render settings
    if legend_elements:
        ax.legend(
            handles=legend_elements,
            loc="upper right",
            fontsize=8,
            frameon=True,
            framealpha=0.9
        )
    ax.set_title(title, fontsize=14, pad=12)
    ax.set_aspect("equal")
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)  # invert y so row 0 is at the top
    ax.axis("off")

    # save graph
    if title:
        os.makedirs("samples", exist_ok=True)
        filename = f"samples/{title}.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")