"""
Author: Priyansh Nayak
Description: Path extracter for maze using best policy 
"""
def extract_path(policy, start, goal):
    # follow policy from start to goal
    path = []
    current = start

    while current is not None:
        path.append(current)

        if current == goal:
            break

        current = policy.get(current)

        # safety check (in case policy is broken)
        if current in path:
            break

    return path