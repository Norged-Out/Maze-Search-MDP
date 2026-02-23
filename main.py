"""
Author: Priyansh Nayak
Description: Entry point for Maze Search + MDP project
"""

from src.experiments.runner import run_experiments
from src.ui.my_game import run_game
import csv


def run_experiment_mode():
    sizes = [10, 20]
    seeds = [1, 2]
    openness_levels = [0.0, 0.1]

    results = run_experiments(sizes, seeds, openness_levels)

    print("Total experiment runs:", len(results))

    # collect union of all keys across all results
    all_keys = set()
    for r in results:
        all_keys.update(r.keys())

    fieldnames = sorted(all_keys)

    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("Wrote results.csv")


if __name__ == "__main__":

    print("Select Mode:")
    print("1 - Run Experiments")
    print("2 - Run Pygame Demo")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        run_experiment_mode()
    elif choice == "2":
        run_game()
    else:
        print("Invalid choice.")