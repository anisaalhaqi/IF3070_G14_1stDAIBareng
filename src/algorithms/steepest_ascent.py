import random
import time

from neighbors import generate_neighbors
from objectives import calculate_objective


def hill_climbing_steepest_ascent(state, max_iterations=1000):
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

        values = [calculate_objective(n) for n in neighbors]
        best_value = max(values)

        if best_value <= current_value:
            stop_reason = "local_optimum"
            break

        best_neighbors = [n for n, v in zip(neighbors, values) if v == best_value]
        current = random.choice(best_neighbors)
        current_value = best_value

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


steepest_ascent = hill_climbing_steepest_ascent
