"""
Author: Priyansh Nayak
Description: MDP solver for Maze using Value Iteration
"""

import time


def value_iteration(maze, gamma=0.9, epsilon=1e-4):
    # start timer
    start_time = time.time()

    # initialise value function (V(s) = 0 for all states)
    V = {}
    for state in maze.all_cells():
        V[state] = 0

    # metrics
    iterations = 0
    state_updates = 0
    final_delta = 0

    # repeat until values converge
    while True:
        delta = 0
        new_V = V.copy()

        for state in maze.all_cells():
            # skip goal (terminal state)
            if state == maze.goal:
                continue

            neighbors = maze.neighbors(state)

            # if no available moves, skip
            if not neighbors:
                continue

            best_value = float("-inf")

            # Bellman update    
            for next_state in neighbors:
                reward = -1  # step cost
                # if next_state == maze.goal:
                #     reward = 10  # goal reward
                value = reward + gamma * V[next_state]

                if value > best_value:
                    best_value = value

            new_V[state] = best_value
            state_updates += 1
            delta = max(delta, abs(new_V[state] - V[state]))
        
        # update metrics
        V = new_V
        iterations += 1
        final_delta = delta

        # stop if change is very small
        if delta < epsilon:
            break

    # extract optimal policy from final values
    policy = {}

    for state in maze.all_cells():
        if state == maze.goal:
            policy[state] = None
            continue

        neighbors = maze.neighbors(state)

        best_action = None
        best_value = float("-inf")

        for next_state in neighbors:
            reward = -1
            value = reward + gamma * V[next_state]

            if value > best_value:
                best_value = value
                best_action = next_state

        policy[state] = best_action

    runtime = time.time() - start_time

    return {
        "policy": policy,
        "values": V,
        "iterations": iterations,
        "state_updates": state_updates,
        "runtime": runtime,
        "memory": len(V),
        "delta": final_delta,
    }