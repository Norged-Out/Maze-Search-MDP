"""
Author: Priyansh Nayak
Description: MDP solver for Maze using Policy Iteration
"""

import time


def policy_iteration(maze, gamma=0.9, epsilon=1e-4):
    # start timer
    start_time = time.time()

    # initialise random policy
    policy = {}
    gr, gc = maze.goal  # cache goal once

    for state in maze.all_cells():
        if state == maze.goal:
            policy[state] = None
            continue

        neighbors = maze.neighbors(state)
        if not neighbors:
            policy[state] = None
            continue

        # initialise policy pointing roughly toward goal
        policy[state] = min(
            neighbors,
            key=lambda n: abs(n[0] - gr) + abs(n[1] - gc)
        )

    # initialise value function
    V = {}
    for state in maze.all_cells():
        V[state] = 0

    goal_reward = 100
    step_cost = -1

    policy_stable = False
    policy_iterations = 0
    evaluation_iterations = 0
    state_updates = 0

    while not policy_stable:

        # Policy Evaluation
        while True:
            delta = 0
            new_V = V.copy()

            for state in maze.all_cells():
                if state == maze.goal:
                    continue

                action = policy[state]
                if action is None:
                    continue

                reward = step_cost
                if action == maze.goal:
                    reward = goal_reward
                value = reward + gamma * V[action]

                new_V[state] = value
                state_updates += 1
                delta = max(delta, abs(new_V[state] - V[state]))

            V = new_V
            evaluation_iterations += 1

            if delta < epsilon:
                break

        # Policy Improvement
        policy_stable = True

        for state in maze.all_cells():
            if state == maze.goal:
                continue

            old_action = policy[state]
            neighbors = maze.neighbors(state)

            best_action = None
            best_value = float("-inf")

            for next_state in neighbors:
                reward = step_cost
                if next_state == maze.goal:
                    reward = goal_reward
                value = reward + gamma * V[next_state]

                if value > best_value:
                    best_value = value
                    best_action = next_state

            policy[state] = best_action

            if best_action != old_action:
                policy_stable = False

        policy_iterations += 1

    runtime = time.time() - start_time

    return {
        "policy": policy,
        "values": V,
        "policy_iterations": policy_iterations,
        "evaluation_iterations": evaluation_iterations,
        "state_updates": state_updates,
        "runtime": runtime,
        "memory": len(V),
    }