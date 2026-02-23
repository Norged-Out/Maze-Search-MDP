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

ALGOS = [
    "DFS",
    "BFS",
    "A* Manhattan",
    "A* Euclidean",
    "MDP: Value Iteration",
    "MDP: Policy Iteration",
]

def run_solver(maze, algo, gamma=0.9, epsilon=1e-4):
    # returns: path (list), explored_order (list), metrics (dict)
    if algo == "DFS":
        res = dfs_solver(maze)
        return res["path"], res.get("explored_order", []), res

    if algo == "BFS":
        res = bfs_solver(maze)
        return res["path"], res.get("explored_order", []), res

    if algo == "A* Manhattan":
        res = astar_solver(maze, heuristic=manhattan)
        return res["path"], res.get("explored_order", []), res

    if algo == "A* Euclidean":
        res = astar_solver(maze, heuristic=euclidean)
        return res["path"], res.get("explored_order", []), res

    if algo == "MDP: Value Iteration":
        res = value_iteration(maze, gamma=gamma, epsilon=epsilon)
        path = extract_path(res["policy"], maze.start, maze.goal)
        return path, [], res

    if algo == "MDP: Policy Iteration":
        res = policy_iteration(maze, gamma=gamma, epsilon=epsilon)
        path = extract_path(res["policy"], maze.start, maze.goal)
        return path, [], res

    raise ValueError(f"Unknown algorithm: {algo}")


def draw_maze(screen, maze, canvas_rect,
              explored_set, path_set):

    # canvas background
    pygame.draw.rect(screen, (245, 245, 245), canvas_rect)

    h, w = maze.height, maze.width

    margin = 20
    inner_w = canvas_rect.width - 2 * margin
    inner_h = canvas_rect.height - 2 * margin

    cell_size = min(inner_w // w, inner_h // h)
    if cell_size < 4:
        cell_size = 4

    # center maze inside canvas
    total_w = w * cell_size
    total_h = h * cell_size

    x0 = canvas_rect.left + (canvas_rect.width - total_w) // 2
    y0 = canvas_rect.top + (canvas_rect.height - total_h) // 2

    # explored
    for (r, c) in explored_set:
        x = x0 + c * cell_size
        y = y0 + r * cell_size
        pygame.draw.rect(screen, (180, 210, 235),
                         (x, y, cell_size, cell_size))

    # path
    for (r, c) in path_set:
        x = x0 + c * cell_size
        y = y0 + r * cell_size
        pygame.draw.rect(screen, (120, 200, 120),
                         (x, y, cell_size, cell_size))

    # walls
    for r in range(h):
        for c in range(w):
            cell = (r, c)
            x = x0 + c * cell_size
            y = y0 + r * cell_size

            if maze.has_wall(cell, "N"):
                pygame.draw.line(screen, (0, 0, 0),
                                 (x, y),
                                 (x + cell_size, y), 2)

            if maze.has_wall(cell, "S"):
                pygame.draw.line(screen, (0, 0, 0),
                                 (x, y + cell_size),
                                 (x + cell_size, y + cell_size), 2)

            if maze.has_wall(cell, "W"):
                pygame.draw.line(screen, (0, 0, 0),
                                 (x, y),
                                 (x, y + cell_size), 2)

            if maze.has_wall(cell, "E"):
                pygame.draw.line(screen, (0, 0, 0),
                                 (x + cell_size, y),
                                 (x + cell_size, y + cell_size), 2)

    # start / goal
    sr, sc = maze.start
    gr, gc = maze.goal

    sx = x0 + sc * cell_size + cell_size // 2
    sy = y0 + sr * cell_size + cell_size // 2
    gx = x0 + gc * cell_size + cell_size // 2
    gy = y0 + gr * cell_size + cell_size // 2

    pygame.draw.circle(screen, (0, 90, 255),
                       (sx, sy), max(3, cell_size // 4))
    pygame.draw.circle(screen, (255, 120, 0),
                       (gx, gy), max(3, cell_size // 4))


def update_animation(path, explored_order, explored_set, path_set, step, mode, speed):
    if speed <= 0:
        return step, mode

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
        if step >= len(path):
            mode = "done"
        else:
            path_set.add(path[step])
            step += 1

    return step, mode

def run_game():
    pygame.init()

    # demo parameters (change these)
    size = 20
    seed = 1
    openness = 0.1
    algo = "BFS"  # DFS, BFS, A*_Manhattan, A*_Euclidean, Value_Iteration, Policy_Iteration

    maze = generate_maze(size, size, seed=seed, openness=openness)
    path, explored_order, metrics = run_solver(maze, algo)
    def rerun_solver():
        nonlocal maze, path, explored_order, metrics
        nonlocal explored_set, path_set, step, mode

        maze = generate_maze(size, size, seed=seed, openness=openness)
        path, explored_order, metrics = run_solver(maze, algo)

        explored_set.clear()
        path_set.clear()
        step = 0
        mode = "explore"

    # fullscreen window
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Maze Demo")

    # gui manager
    manager = pygame_gui.UIManager((screen_w, screen_h))

    # sidebar panel
    sidebar_w = 320
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, sidebar_w, screen_h),
        manager=manager,
    )
    pad = 20
    y = pad

    # solver label
    solver_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Solver",
        manager=manager,
        container=panel,
    )
    y += 30

    # solver dropdown
    solver_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list = list(ALGOS),
        starting_option=algo,
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 36),
        manager=manager,
        container=panel,
    )
    y += 50

    # run button
    run_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 40),
        text="Run",
        manager=manager,
        container=panel,
    )

    # maze drawing area (everything to the right of sidebar)
    canvas_rect = pygame.Rect(sidebar_w, 0, screen_w - sidebar_w, screen_h)

    font = pygame.font.SysFont(None, 22)
    clock = pygame.time.Clock()
    time_delta = 0

    explored_set = set()
    path_set = set()

    # animation state
    step = 0
    mode = "explore"  # explore -> path -> done
    speed = 20        # explored cells per second-ish

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keyboard inputs
            if event.type == pygame.KEYDOWN:       
                # esc to stop
                if event.key == pygame.K_ESCAPE:
                    running = False
                # toggle pause by setting speed to 0 / restoring
                elif event.key == pygame.K_SPACE:
                    speed = 0 if speed > 0 else 20                
                # quick restart animation
                elif event.key == pygame.K_r:
                    explored_set.clear()
                    path_set.clear()
                    step = 0
                    mode = "explore"
                    speed = 20

            # run solver
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == run_button:
                    selected = solver_dropdown.selected_option
                    algo = selected[0] if isinstance(selected, tuple) else selected
                    rerun_solver()

            manager.process_events(event)

        # advance animation
        step, mode = update_animation(
            path, explored_order, explored_set,
            path_set, step, mode, speed
        )

        # draw
        screen.fill((30, 30, 30))
        draw_maze(screen, maze, canvas_rect,
          explored_set, path_set)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()