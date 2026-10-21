import random
import time

from neighbors import generate_neighbors
from objectives import calculate_objective


def stochastic_hill_climbing(state, max_iterations=1000):
    start = time.time()

    current = state
    current_value = calculate_objective(current)

    value_history = [current_value]
    iteration = 0
    stop_reason = "max_iterations"

    while iteration < max_iterations:
        neighbors = generate_neighbors(current)

        if not neighbors:
            stop_reason = "no_neighbor"
            break

        better = []
        for n in neighbors:
            v = calculate_objective(n)
            if v > current_value:
                better.append((n, v))

        if not better:
            stop_reason = "local_optimum"
            break

        current, current_value = random.choice(better)

        value_history.append(current_value)
        iteration += 1

    return {
        "initial_state": state,
        "final_state": current,
        "final_value": current_value,
        "value_history": value_history,
        "iterations": iteration,
        "stop_reason": stop_reason,
        "duration": time.time() - start,
    }