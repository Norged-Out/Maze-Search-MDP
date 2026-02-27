"""
Author: Priyansh Nayak
Description: Entry point for Maze Search + MDP project
"""

from src.experiments.runner import run_experiments
from src.experiments.analysis import run_analysis
from src.experiments.samples import generate_samples
from src.ui.my_game import run_game
import csv
import os

def write_results(filename, results):
    os.makedirs("results", exist_ok=True)

    filepath = os.path.join("results", filename)

    print(f"Total runs for {filename}: {len(results)}")

    all_keys = set()
    for r in results:
        all_keys.update(r.keys())

    fieldnames = sorted(all_keys)

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {filepath}")

def run_experiment_mode():

    # -------------------------
    # Size Scaling
    # -------------------------
    sizes = [10, 20, 30, 40, 50]
    seeds = [1, 2, 3]
    openness = [0.1]

    results_scaling = run_experiments(
        sizes,
        seeds,
        openness,
        gammas=(0.9,),
        goal_rewards=(100,),
        step_costs=(-1,),
    )

    write_results("results_scaling.csv", results_scaling)

    # -------------------------
    # Openness Study
    # -------------------------
    sizes = [30]
    seeds = [1, 2, 3]
    openness = [0.0, 0.1, 0.2, 0.3]

    results_openness = run_experiments(
        sizes,
        seeds,
        openness,
        gammas=(0.9,),
        goal_rewards=(100,),
        step_costs=(-1,),
    )

    write_results("results_openness.csv", results_openness)

    # -------------------------
    # Gamma Study (MDP focus)
    # -------------------------
    sizes = [30]
    seeds = [1]
    openness = [0.1]

    results_gamma = run_experiments(
        sizes,
        seeds,
        openness,
        gammas=(0.7, 0.8, 0.9, 0.95, 0.99),
        goal_rewards=(100,),
        step_costs=(-1,),
    )

    write_results("results_gamma.csv", results_gamma)

    print("All experiment blocks completed.")


if __name__ == "__main__":

    print("Select Mode:")    
    print("1 - Run Pygame Demo")
    print("2 - Generate Samples")
    print("3 - Run Experiments")
    print("4 - Run Analysis")

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "1":            
            run_game()
        elif choice == "2":
            generate_samples()
        elif choice == "3":
            run_experiment_mode()
        elif choice == "4":
            run_analysis()
        else:
            print("Invalid choice.")
            break