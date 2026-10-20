import math
import random
import time

from neighbors import random_neighbor
from objectives import calculate_objective

def simulated_annealing(state, initial_temp=100.0, min_temp=1.0,
                        stuck_limit=50, max_iterations=5000):
    start = time.time()
    cooling_rate = (min_temp / initial_temp) ** (1.0 / max_iterations)

    current = state
    current_value = calculate_objective(current)
    best, best_value = current, current_value

    value_history = [current_value]
    probability_history = []

    temp = initial_temp
    iteration = 0
    no_improvement = 0
    stuck_count = 0

    while temp > min_temp and iteration < max_iterations:
        neighbor = random_neighbor(current)

        if neighbor is not None:
            delta = calculate_objective(neighbor) - current_value
            probability = 1.0 if delta >= 0 else math.exp(delta / temp)
            probability_history.append(probability)

            if random.random() < probability:
                current = neighbor
                current_value += delta

        if current_value > best_value:
            best, best_value = current, current_value
            no_improvement = 0
        else:
            no_improvement += 1
            if no_improvement >= stuck_limit:
                stuck_count += 1
                no_improvement = 0

        value_history.append(current_value)
        temp *= cooling_rate
        iteration += 1

    return {
        "initial_state": state,
        "final_state": best,
        "final_value": best_value,
        "value_history": value_history,
        "probability_history": probability_history,
        "duration": time.time() - start,
        "iterations": iteration,
        "stuck_count": stuck_count,
    }