import random
import time

from neighbors import generate_neighbors
from objectives import calculate_objective
from state import State


def random_restart_hill_climbing(state, max_restarts=10, max_iterations_per_restart=1000, vehicles=None):
    start_time = time.time()

    max_restarts = max(1, int(max_restarts))
    max_iterations_per_restart = max(1, int(max_iterations_per_restart))

    ship = state.ship
    if vehicles is None:
        vehicles = [p.vehicle for p in state.placements]

    best_state = state.copy()
    best_value = calculate_objective(best_state)

    value_history = []
    best_value_history = []
    restart_indices = []
    iterations_per_restart = []
    restart_details = []

    for r in range(max_restarts):
        if r == 0:
            current = state.copy()
        else:
            current = State.random(ship, vehicles)

        current_value = calculate_objective(current)

        restart_indices.append(len(value_history))
        value_history.append(current_value)

        if current_value > best_value:
            best_value = current_value
            best_state = current.copy()

        best_value_history.append(best_value)

        restart_iteration = 0
        restart_stop_reason = "max_iterations"

        while restart_iteration < max_iterations_per_restart:
            neighbors = generate_neighbors(current)

            if not neighbors:
                restart_stop_reason = "no_neighbor"
                break

            values = [calculate_objective(n) for n in neighbors]
            best_neighbor_val = max(values)

            if best_neighbor_val <= current_value:
                restart_stop_reason = "local_optimum"
                break

            best_neighbors = [n for n, v in zip(neighbors, values) if v == best_neighbor_val]
            current = random.choice(best_neighbors)
            current_value = best_neighbor_val

            restart_iteration += 1
            value_history.append(current_value)

            if current_value > best_value:
                best_value = current_value
                best_state = current.copy()

            best_value_history.append(best_value)

        iterations_per_restart.append(restart_iteration)
        restart_details.append({
            "restart": r + 1,
            "final_value": current_value,
            "iterations": restart_iteration,
            "stop_reason": restart_stop_reason,
        })

    stop_reason = "max_restarts"
    duration = time.time() - start_time

    return {
        "initial_state": state,
        "final_state": best_state,
        "final_value": best_value,
        "value_history": value_history,
        "best_value_history": best_value_history,
        "restart_indices": restart_indices,
        "restarts": max_restarts,
        "max_restarts": max_restarts,
        "iterations_per_restart": iterations_per_restart,
        "iterations": sum(iterations_per_restart),
        "stop_reason": stop_reason,
        "restart_details": restart_details,
        "duration": duration,
    }


random_restart = random_restart_hill_climbing
hill_climbing_random_restart = random_restart_hill_climbing
