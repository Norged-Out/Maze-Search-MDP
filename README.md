# Maze_Search_MDP

Implementation and comparative analysis of classical search algorithms and Markov Decision Process (MDP) methods for maze solving.

This project was developed for **CS7IS2 – Artificial Intelligence** and includes:

* Custom maze generation
* DFS, BFS, A* (Manhattan & Euclidean)
* Value Iteration
* Policy Iteration
* Automated experiments
* Performance analysis and visualisation
* Interactive Pygame demo

---

## Overview

The objective of this project is to compare fundamentally different approaches to solving deterministic shortest-path problems in grid mazes.

Two paradigms are evaluated:

### Search-Based Planning

* Depth-First Search (DFS)
* Breadth-First Search (BFS)
* A* Search (Manhattan heuristic)
* A* Search (Euclidean heuristic)

### MDP-Based Planning

* Value Iteration
* Policy Iteration

Experiments compare scalability, runtime, memory usage, and computational effort across varying maze sizes and openness levels.

---

## Features

* Custom recursive backtracking maze generator
* Adjustable maze size
* Adjustable openness parameter (controls loop density)
* Deterministic reproducibility via seeds
* Full experimental pipeline (CSV output)
* Automated plotting of performance metrics
* Interactive visual demo via Pygame
* Clean modular solver implementations

---

## Installation

Python 3.10+ recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

### requirements.txt

```
pygame-ce>=2.5
pygame_gui>=0.6
matplotlib>=3.8
numpy>=1.26
pandas>=2.1
```

Optional virtual environment:

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

## Running the Project

All functionality is controlled from:

```bash
python main.py
```

You will see:

```
1 - Run Pygame Demo
2 - Generate Samples
3 - Run Experiments
4 - Run Analysis
```

---

## Modes

### 1 — Run Pygame Demo

Launches an interactive graphical demo.

* Generates maze
* Runs selected solver
* Visualises exploration and final path
* Used for demonstration video

---

### 2 — Generate Samples

Generates static rendered images and saves them to:

```
/samples
```

Includes:

* Unsolved maze
* Search solutions
* MDP policy visualisations
* Size comparison examples
* Openness comparison examples

---

### 3 — Run Experiments

Runs automated performance experiments across:

* Multiple maze sizes
* Multiple openness levels
* Multiple random seeds

Outputs CSV files to:

```
/results
```

Metrics recorded:

* Runtime
* Nodes expanded
* Maximum data structure size
* Iterations (MDP)
* State updates (MDP)

---

### 4 — Run Analysis

Reads CSV experiment results and generates plots.

Outputs figures to:

```
/figures
```

Includes:

* Search work vs size
* Search memory vs size
* Search runtime vs openness
* Search runtime vs work
* MDP work vs size
* MDP runtime vs openness
* Gamma sensitivity
* Log-scale runtime comparison (all algorithms)

---

## Individual Algorithm Usage

All solver implementations are modular and located in:

```
src/solvers/
```

Each can be imported and used independently.

### DFS

```python
from src.solvers.dfs import dfs_solver
result = dfs_solver(maze)
path = result["path"]
explored = result["explored"]
```

### BFS

```python
from src.solvers.bfs import bfs_solver
result = bfs_solver(maze)
```

### A* (Manhattan)

```python
from src.solvers.astar import astar_solver, manhattan
result = astar_solver(maze, manhattan)
```

### A* (Euclidean)

```python
from src.solvers.astar import astar_solver, euclidean
result = astar_solver(maze, euclidean)
```

### Value Iteration

```python
from src.solvers.value_iter import value_iteration
result = value_iteration(maze)
policy = result["policy"]
```

### Policy Iteration

```python
from src.solvers.policy_iter import policy_iteration
result = policy_iteration(maze)
```

Path extraction for MDP methods:

```python
from src.solvers.utils import extract_path
path = extract_path(policy, maze.start, maze.goal)
```

---

## Project Structure

```
src/
    maze/
        generator.py
        render.py
        maze.py
    solvers/
        dfs.py
        bfs.py
        astar.py
        value_iter.py
        policy_iter.py
        utils.py
    experiments/
        runner.py
        analysis.py
        samples.py
    ui/
        my_game.py

figures/        # Generated plots
results/        # CSV experiment outputs
samples/        # Rendered maze images
main.py         # Entry point
requirements.txt
README.md
```

---

## Experimental Design

Experiments evaluate:

* Maze sizes: 10×10 to 50×50
* Openness levels: 0.0 to 0.3
* Multiple random seeds

Comparisons are made using:

* Runtime
* Nodes expanded
* Maximum data structure size
* Total state updates (MDP)
* Iterations to convergence

---

## Submission Contents

The submission ZIP includes:

* All Python source code
* `README.txt`
* `requirements.txt`
* `/results` CSV files
* `/figures` performance plots
* `/samples` rendered examples
* PDF performance analysis report
* Demo video

---

## Design Philosophy

* Explicit algorithm implementations
* Reproducible experiments
* Clear separation between search and MDP paradigms
* Modular solver design
* Deterministic maze generation
* Full experimental pipeline

---

## License

Educational use only.