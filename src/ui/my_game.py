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
    size = max(6, cell_size // 2)
    pygame.draw.line(
        screen,
        (255, 120, 0),
        (gx - size//2, gy - size//2),
        (gx + size//2, gy + size//2),
        3,
    )

    pygame.draw.line(
        screen,
        (255, 120, 0),
        (gx - size//2, gy + size//2),
        (gx + size//2, gy - size//2),
        3,
    )


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

    # -------------------------
    # Application State
    # -------------------------
    state = {
        "size": 20,
        "seed": 1,
        "openness": 0.1,
        "algo": "BFS",

        "maze": None,
        "path": [],
        "explored_order": [],
        "metrics": {},

        "explored_set": set(),
        "path_set": set(),

        "step": 0,
        "mode": "explore",
        "speed": 20,

        "gamma": 0.9,
    }

    # -------------------------
    # Window Setup
    # -------------------------
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Maze Demo")

    manager = pygame_gui.UIManager((screen_w, screen_h))

    # -------------------------
    # Sidebar UI
    # -------------------------
    sidebar_w = 320
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, sidebar_w, screen_h),
        manager=manager,
    )

    pad = 20
    y = pad

    # ---- Maze Parameters ----

    # Size label
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Maze Size (N x N)",
        manager=manager,
        container=panel,
    )
    y += 30

    # Size input
    size_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 32),
        manager=manager,
        container=panel,
    )
    size_input.set_text(str(state["size"]))
    y += 50

    # Seed label
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Seed",
        manager=manager,
        container=panel,
    )
    y += 30

    # Seed input
    seed_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 32),
        manager=manager,
        container=panel,
    )
    seed_input.set_text(str(state["seed"]))
    y += 50

    # Openness label
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Openness (0.0 - 0.3)",
        manager=manager,
        container=panel,
    )
    y += 30

    # Openness slider (0–30 mapped to 0.00–0.30)
    openness_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        start_value=int(state["openness"] * 100),
        value_range=(0, 30),
        manager=manager,
        container=panel,
    )
    y += 40

    # Generate button
    generate_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 40),
        text="Generate Maze",
        manager=manager,
        container=panel,
    )
    y += 50

    # ---- Solver Section ----

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Solver",
        manager=manager,
        container=panel,
    )
    y += 30

    solver_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=list(ALGOS),
        starting_option=state["algo"],
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 36),
        manager=manager,
        container=panel,
    )
    y += 40

    # Gamma label
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Gamma (MDP only)",
        manager=manager,
        container=panel,
    )
    y += 30

    gamma_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 32),
        manager=manager,
        container=panel,
    )
    gamma_input.set_text("0.9")
    y += 50

    run_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 40),
        text="Run Solver",
        manager=manager,
        container=panel,
    )
    y += 60

    # ---- Stats Section ----
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(pad, y, sidebar_w - 2 * pad, 24),
        text="Stats",
        manager=manager,
        container=panel,
    )
    y += 30

    stats_box = pygame_gui.elements.UITextBox(
        html_text="No solution yet.",
        relative_rect=pygame.Rect(
            pad,
            y,
            sidebar_w - 2 * pad,
            screen_h - y - 20
        ),
        manager=manager,
        container=panel,
    )

    # -------------------------
    # Canvas
    # -------------------------
    canvas_rect = pygame.Rect(sidebar_w, 0, screen_w - sidebar_w, screen_h)
    clock = pygame.time.Clock()

    # -------------------------
    # Helper Functions
    # -------------------------

    def reset_animation():
        state["explored_set"].clear()
        state["path_set"].clear()
        state["step"] = 0
        state["mode"] = "explore"

    def generate_maze_only():
        state["maze"] = generate_maze(
            state["size"],
            state["size"],
            seed=state["seed"],
            openness=state["openness"],
        )

        state["path"] = []
        state["explored_order"] = []
        state["metrics"] = {}
        reset_animation()

    def rerun_solver():
        if state["maze"] is None:
            return

        path, explored, metrics = run_solver(
            state["maze"],
            state["algo"],
            gamma=state["gamma"],
        )

        state["path"] = path
        state["explored_order"] = explored
        state["metrics"] = metrics

        reset_animation()

        # build stats text
        moves = max(0, len(state["path"]) - 1)

        lines = [
            f"<b>Algorithm:</b> {state['algo']}",
            f"<b>Moves:</b> {moves}",
        ]

        if "runtime" in state["metrics"]:
            lines.append(f"<b>Runtime:</b> {state['metrics']['runtime']:.6f}s")

        if "nodes_expanded" in state["metrics"]:
            lines.append(f"<b>Nodes Expanded:</b> {state['metrics']['nodes_expanded']}")

        if "state_updates" in state["metrics"]:
            lines.append(f"<b>State Updates:</b> {state['metrics']['state_updates']}")

        if "memory" in state["metrics"]:
            lines.append(f"<b>Memory:</b> {state['metrics']['memory']}")

        if "iterations" in state["metrics"]:
            lines.append(f"<b>Iterations:</b> {state['metrics']['iterations']}")

        if "policy_iterations" in state["metrics"]:
            lines.append(f"<b>Policy Iterations:</b> {state['metrics']['policy_iterations']}")

        if "evaluation_iterations" in state["metrics"]:
            lines.append(f"<b>Eval Iterations:</b> {state['metrics']['evaluation_iterations']}")

        stats_box.set_text("<br>".join(lines))

    # -------------------------
    # Main Loop
    # -------------------------
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Keyboard Controls
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    state["speed"] = 0 if state["speed"] > 0 else 20

                elif event.key == pygame.K_r:
                    reset_animation()

            # Button Events
            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == generate_button:
                    # update state from UI
                    try:
                        state["size"] = max(2, min(50, int(size_input.get_text())))
                    except:
                        state["size"] = 20
                        size_input.set_text("20")

                    try:
                        state["seed"] = int(seed_input.get_text())
                    except:
                        state["seed"] = 1
                        seed_input.set_text("1")

                    state["openness"] = openness_slider.get_current_value() / 100.0

                    generate_maze_only()

                elif event.ui_element == run_button:
                    try:
                        g = float(gamma_input.get_text())
                        state["gamma"] = max(0.0, min(0.999, g))
                    except:
                        state["gamma"] = 0.9
                        gamma_input.set_text("0.9")
                    selected = solver_dropdown.selected_option
                    state["algo"] = selected[0] if isinstance(selected, tuple) else selected
                    rerun_solver()

            manager.process_events(event)

        # -------------------------
        # Animation Update
        # -------------------------
        if state["maze"] is not None:
            state["step"], state["mode"] = update_animation(
                state["path"],
                state["explored_order"],
                state["explored_set"],
                state["path_set"],
                state["step"],
                state["mode"],
                state["speed"],
            )

        # -------------------------
        # Drawing
        # -------------------------
        screen.fill((30, 30, 30))

        if state["maze"] is not None:
            draw_maze(
                screen,
                state["maze"],
                canvas_rect,
                state["explored_set"],
                state["path_set"],
            )

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()