"""
Author: Priyansh Nayak
Description: Loads experiment CSVs, aggregates metrics, and saves plots
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)


def save_fig(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, name))
    plt.close()


def load_data():
    scaling = pd.read_csv("results/results_scaling.csv")
    openness = pd.read_csv("results/results_openness.csv")
    gamma = pd.read_csv("results/results_gamma.csv")
    return scaling, openness, gamma

def mean_by(df, group_cols):
    return df.groupby(group_cols, as_index=False).mean(numeric_only=True)

def plot_runtime_vs_size(scaling_df, log_scale=True):
    df = mean_by(scaling_df, ["size", "algorithm"])

    pivot = df.pivot(index="size", columns="algorithm", values="runtime")

    ax = pivot.plot(kind="bar", figsize=(8,5))
    ax.set_ylabel("Runtime (s)")
    ax.set_title("Runtime vs Maze Size")

    if log_scale:
        ax.set_yscale("log")

    save_fig("runtime_vs_size.png")


def plot_search_work_vs_size(scaling_df):
    search = scaling_df[
        scaling_df["algorithm"].isin(["DFS", "BFS", "A*_Manhattan", "A*_Euclidean"])
    ]

    df = mean_by(search, ["size", "algorithm"])

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["size"], subset["work"], marker="o", label=algo)

    plt.xlabel("Maze Size")
    plt.ylabel("Nodes Expanded")
    plt.title("Search Work vs Size")
    plt.legend()
    save_fig("search_work_vs_size.png")


def plot_mdp_work_vs_size(scaling_df):
    mdp = scaling_df[
        scaling_df["algorithm"].isin(["Value_Iteration", "Policy_Iteration"])
    ]

    df = mean_by(mdp, ["size", "algorithm"])

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["size"], subset["work"], marker="o", label=algo)

    plt.xlabel("Maze Size")
    plt.ylabel("State Updates")
    plt.title("MDP Work vs Size")
    plt.legend()
    save_fig("mdp_work_vs_size.png")


def runtime_summary_table(scaling_df, size=50):
    df = scaling_df[scaling_df["size"] == size]

    summary = (
        df.groupby("algorithm")["runtime"]
        .agg(["mean", "std"])
        .reset_index()
        .sort_values("mean")
    )

    summary["cv"] = summary["std"] / summary["mean"]

    print("\nRuntime Summary (Size = {})".format(size))
    print(summary.to_string(index=False))


def plot_search_runtime_vs_work(scaling_df):
    search = scaling_df[
        scaling_df["algorithm"].isin(["DFS", "BFS", "A*_Manhattan", "A*_Euclidean"])
    ]

    for algo in search["algorithm"].unique():
        subset = search[search["algorithm"] == algo]
        plt.scatter(subset["work"], subset["runtime"], label=algo)

    plt.xlabel("Nodes Expanded")
    plt.ylabel("Runtime (s)")
    plt.title("Search: Runtime vs Work")
    plt.legend()
    save_fig("search_runtime_vs_work.png")


def plot_search_memory_vs_size(scaling_df):
    search = scaling_df[
        scaling_df["algorithm"].isin(["DFS", "BFS", "A*_Manhattan", "A*_Euclidean"])
    ]

    df = mean_by(search, ["size", "algorithm"])
    pivot = df.pivot(index="size", columns="algorithm", values="memory")

    pivot.plot(kind="bar", figsize=(8,5))
    plt.ylabel("Max Frontier Size")
    plt.title("Search Memory vs Size")
    save_fig("search_memory_vs_size.png")


def plot_search_runtime_vs_openness(openness_df):
    search = openness_df[
        openness_df["algorithm"].isin(
            ["DFS", "BFS", "A*_Manhattan", "A*_Euclidean"]
        )
    ]

    df = search.groupby(["openness", "algorithm"], as_index=False).mean(numeric_only=True)

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["openness"], subset["runtime"], marker="o", label=algo)

    plt.xlabel("Openness")
    plt.ylabel("Runtime (s)")
    plt.title("Search: Runtime vs Openness")
    plt.legend()
    save_fig("search_runtime_vs_openness.png")

def plot_mdp_runtime_vs_openness(openness_df):
    mdp = openness_df[
        openness_df["algorithm"].isin(
            ["Value_Iteration", "Policy_Iteration"]
        )
    ]

    df = mdp.groupby(["openness", "algorithm"], as_index=False).mean(numeric_only=True)

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["openness"], subset["runtime"], marker="o", label=algo)

    plt.xlabel("Openness")
    plt.ylabel("Runtime (s)")
    plt.title("MDP: Runtime vs Openness")
    plt.legend()
    save_fig("mdp_runtime_vs_openness.png")

def plot_gamma_sensitivity(gamma_df):
    mdp = gamma_df[
        gamma_df["algorithm"].isin(["Value_Iteration", "Policy_Iteration"])
    ]

    for algo in mdp["algorithm"].unique():
        subset = mdp[mdp["algorithm"] == algo]
        plt.plot(subset["gamma"], subset["runtime"], marker="o", label=algo)

    plt.xlabel("Gamma")
    plt.ylabel("Runtime (s)")
    plt.title("Gamma Sensitivity (MDP)")
    plt.legend()
    save_fig("gamma_sensitivity.png")

def run_analysis():
    scaling, openness, gamma_df = load_data()
    plot_runtime_vs_size(scaling)
    plot_search_work_vs_size(scaling)
    plot_mdp_work_vs_size(scaling)
    runtime_summary_table(scaling, size=50)
    plot_search_runtime_vs_work(scaling)
    plot_search_memory_vs_size(scaling)
    plot_search_runtime_vs_openness(openness)
    plot_mdp_runtime_vs_openness(openness)
    plot_gamma_sensitivity(gamma_df)