"""
Author: Priyansh Nayak
Description: Stores the structure of a maze
"""
from typing import Dict, List, Tuple, Iterable
from dataclasses import dataclass

# Rules
Cell = Tuple[int, int] # (row, col)
N, E, S, W = "N", "E", "S", "W"
DIRS = (N, E, S, W) # directions

# How each direction changes
DELTAS: Dict[str, Tuple[int, int]] = {
    N: (-1, 0),
    E: (0, 1),
    S: (1, 0),
    W: (0, -1),
}

OPPOSITE = {N: S, E: W, S: N, W: E}

@dataclass
class Maze:
    height: int
    width: int
    start: Cell = (0, 0)
    goal: Cell = None # type: ignore
    walls: List[List[Dict[str, bool]]] = None  # type: ignore

    def __post_init__(self):
        if self.height <= 0 or self.width <= 0:
            raise ValueError("Maze height and width must be positive integers.")

        if self.goal is None:
            self.goal = (self.height - 1, self.width - 1)

        # Initialize every cell with all walls present
        self.walls = [
            [{d: True for d in DIRS} for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # Sanity-check start/goal
        if not self.in_bounds(self.start):
            raise ValueError(f"Start {self.start} is out of bounds.")
        if not self.in_bounds(self.goal):
            raise ValueError(f"Goal {self.goal} is out of bounds.")
        
    def in_bounds(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.height and 0 <= c < self.width

    def has_wall(self, cell: Cell, direction: str) -> bool:
        r, c = cell
        return self.walls[r][c][direction]
    
    def remove_wall(self, cell: Cell, direction: str) -> None:
        """
        Remove the wall from `cell` in `direction`,
        and remove the opposite wall from the neighboring cell.
        """
        if direction not in DIRS:
            raise ValueError(f"Invalid direction: {direction}")

        r, c = cell
        dr, dc = DELTAS[direction]
        nr, nc = r + dr, c + dc
        neighbor = (nr, nc)

        if not self.in_bounds(neighbor):
            raise ValueError(f"Cannot remove wall {direction} from {cell}: neighbor out of bounds.")

        # Remove wall in current cell
        self.walls[r][c][direction] = False
        # Remove opposite wall in neighbor cell
        self.walls[nr][nc][OPPOSITE[direction]] = False

    def neighbors(self, cell: Cell) -> List[Cell]:
        """
        Return reachable neighbors from this cell (no wall blocking).
        """
        r, c = cell
        result: List[Cell] = []
        for d in DIRS:
            if not self.walls[r][c][d]:  # no wall => passage
                dr, dc = DELTAS[d]
                nxt = (r + dr, c + dc)
                if self.in_bounds(nxt):
                    result.append(nxt)
        return result
    
    def all_cells(self) -> Iterable[Cell]:
        for r in range(self.height):
            for c in range(self.width):
                yield (r, c)