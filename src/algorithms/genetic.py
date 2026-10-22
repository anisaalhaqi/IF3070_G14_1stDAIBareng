import random
import time

from constraints import is_valid
from neighbors import random_neighbor
from objectives import calculate_objective
from state import State, Placement 

def crossover(p1, p2):
    n = len(p1.placements)
    child = State(p1.ship, [Placement(pl.vehicle, pl.Orientation) for pl in p1.placements])
    order = list(range(n))
    random.shuffle(order)
    for i in order:
        parents = [p1, p2]
        random.shuffle(parents)
        for parent in parents:
            src = parent.placements[i]
            if not src.on_ship:
                continue
            dst = child.placements[i]
            dst.Orientation, dst.x, dst.y, dst.on_ship = src.Orientation, src.x, src.y, True
            if is_valid(child):
                break
            dst.on_ship, dst.x, dst.y = False, None, None
    return child


def mutate(state, mutation_rate):
    if random.random() < mutation_rate:
        neighbor = random_neighbor(state)
        if neighbor is not None:
            return neighbor
    return state


def random_roulette_wheel(population, fitness, k=3):
    idx = random.sample(range(len(population)), min(k, len(population)))
    return population[max(idx, key=lambda i: fitness[i])]


def genetic_algorithm(state, population_size=50, max_iterations=100,
                      mutation_rate=0.3, elite_count=1):
    start = time.time()
    vehicles = [p.vehicle for p in state.placements]
    population = [state.copy()]
    while len(population) < population_size:
        population.append(State.random(state.ship, vehicles))

    fitness = [calculate_objective(s) for s in population]

    best_idx = max(range(len(population)), key=lambda i: fitness[i])
    best, best_value = population[best_idx].copy(), fitness[best_idx]

    max_history = [max(fitness)]
    avg_history = [sum(fitness) / len(fitness)]

    for _ in range(max_iterations):
        ranked = sorted(range(len(population)), key=lambda i: fitness[i], reverse=True)
        new_pop = [population[i].copy() for i in ranked[:elite_count]]

        while len(new_pop) < population_size:
            p1 = random_roulette_wheel(population, fitness)
            p2 = random_roulette_wheel(population, fitness)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_pop.append(child)

        population = new_pop
        fitness = [calculate_objective(s) for s in population]

        gen_best = max(range(len(population)), key=lambda i: fitness[i])
        if fitness[gen_best] > best_value:
            best, best_value = population[gen_best].copy(), fitness[gen_best]

        max_history.append(max(fitness))
        avg_history.append(sum(fitness) / len(fitness))

    return {
        "initial_state": state,
        "final_state": best,
        "final_value": best_value,
        "max_history": max_history,
        "avg_history": avg_history,
        "population_size": population_size,
        "iterations": max_iterations,
        "duration": time.time() - start,
    }