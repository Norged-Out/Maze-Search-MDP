"""
Author: Priyansh Nayak
Description: Pygame demo UI to animate maze solving
"""

import pygame
import pygame_gui

from src.maze.generator import generate_maze
from src.solvers.dfs import dfs_solver
from src.solvers.bfs import bfs_solver
from src.solvers.astar import astar_solver, manhattan, euclidean
from src.solvers.value_iter import value_iteration
from src.solvers.policy_iter import policy_iteration
from src.solvers.utils import extract_path




def run_solver(maze, algo, gamma=0.9, epsilon=1e-4):
    # returns: path (list), explored_order (list), metrics (dict)
    if algo == "DFS":
        res = dfs_solver(maze)
        return res["path"], res.get("explored_order", []), res

    if algo == "BFS":
        res = bfs_solver(maze)
        return res["path"], res.get("explored_order", []), res

    if algo == "A*_Manhattan":
        res = astar_solver(maze, heuristic=manhattan)
        return res["path"], res.get("explored_order", []), res

    if algo == "A*_Euclidean":
        res = astar_solver(maze, heuristic=euclidean)
        return res["path"], res.get("explored_order", []), res

    if algo == "Value_Iteration":
        res = value_iteration(maze, gamma=gamma, epsilon=epsilon)
        path = extract_path(res["policy"], maze.start, maze.goal)
        return path, [], res

    if algo == "Policy_Iteration":
        res = policy_iteration(maze, gamma=gamma, epsilon=epsilon)
        path = extract_path(res["policy"], maze.start, maze.goal)
        return path, [], res

    raise ValueError(f"Unknown algorithm: {algo}")


def draw_maze(screen, maze, cell_size, margin, explored_set, path_set):
    h, w = maze.height, maze.width

    # background
    screen.fill((245, 245, 245))

    # explored overlay
    for (r, c) in explored_set:
        x = margin + c * cell_size
        y = margin + r * cell_size
        pygame.draw.rect(screen, (180, 210, 235), (x, y, cell_size, cell_size))

    # path overlay
    for (r, c) in path_set:
        x = margin + c * cell_size
        y = margin + r * cell_size
        pygame.draw.rect(screen, (120, 200, 120), (x, y, cell_size, cell_size))

    # draw walls
    for r in range(h):
        for c in range(w):
            cell = (r, c)
            x = margin + c * cell_size
            y = margin + r * cell_size

            if maze.has_wall(cell, "N"):
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x + cell_size, y), 2)
            if maze.has_wall(cell, "S"):
                pygame.draw.line(screen, (0, 0, 0), (x, y + cell_size), (x + cell_size, y + cell_size), 2)
            if maze.has_wall(cell, "W"):
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + cell_size), 2)
            if maze.has_wall(cell, "E"):
                pygame.draw.line(screen, (0, 0, 0), (x + cell_size, y), (x + cell_size, y + cell_size), 2)

    # start / goal markers
    sr, sc = maze.start
    gr, gc = maze.goal

    sx = margin + sc * cell_size + cell_size // 2
    sy = margin + sr * cell_size + cell_size // 2
    gx = margin + gc * cell_size + cell_size // 2
    gy = margin + gr * cell_size + cell_size // 2

    pygame.draw.circle(screen, (0, 90, 255), (sx, sy), max(3, cell_size // 4))
    pygame.draw.circle(screen, (255, 120, 0), (gx, gy), max(3, cell_size // 4))


def run_game():
    pygame.init()

    # demo parameters (change these)
    size = 20
    seed = 1
    openness = 0.1
    algo = "BFS"  # DFS, BFS, A*_Manhattan, A*_Euclidean, Value_Iteration, Policy_Iteration

    maze = generate_maze(size, size, seed=seed, openness=openness)
    path, explored_order, metrics = run_solver(maze, algo)

    cell_size = 22
    margin = 20
    width = margin * 2 + maze.width * cell_size
    height = margin * 2 + maze.height * cell_size + 60  # extra space for text

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Demo")

    font = pygame.font.SysFont(None, 22)
    clock = pygame.time.Clock()

    explored_set = set()
    path_set = set()

    # animation state
    step = 0
    mode = "explore"  # explore -> path -> done
    speed = 20        # explored cells per second-ish

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # toggle pause by setting speed to 0 / restoring
                    speed = 0 if speed > 0 else 20

                if event.key == pygame.K_r:
                    # quick restart animation
                    explored_set.clear()
                    path_set.clear()
                    step = 0
                    mode = "explore"
                    speed = 20

        # advance animation
        if speed > 0:
            if mode == "explore":
                if explored_order:
                    add_count = max(1, speed // 10)
                    for _ in range(add_count):
                        if step >= len(explored_order):
                            mode = "path"
                            step = 0
                            break
                        explored_set.add(explored_order[step])
                        step += 1
                else:
                    mode = "path"
                    step = 0

            elif mode == "path":
                add_count = 1
                for _ in range(add_count):
                    if step >= len(path):
                        mode = "done"
                        break
                    path_set.add(path[step])
                    step += 1

        # draw
        draw_maze(screen, maze, cell_size, margin, explored_set, path_set)

        # info text
        info = f"{algo} | size={size} seed={seed} open={openness} | moves={max(0, len(path)-1)}"
        text = font.render(info, True, (0, 0, 0))
        screen.blit(text, (margin, margin + maze.height * cell_size + 20))

        hint = "SPACE: pause/resume   R: restart   close window to quit"
        text2 = font.render(hint, True, (0, 0, 0))
        screen.blit(text2, (margin, margin + maze.height * cell_size + 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()