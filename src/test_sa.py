import random
from constraints import is_valid
from data.loader import load_data
from state import State
from algorithms.simulated_annealing import simulated_annealing
from objectives import calculate_objective

ship, vehicles = load_data("data/data.json")

for seed in (1, 2, 3):
    random.seed(seed)
    initial = State.random(ship, vehicles)
    r = simulated_annealing(initial)
    print(f"seed={seed} initial={calculate_objective(initial)} "
              f"final={r['final_value']} iter={r['iterations']} "
              f"stuck={r['stuck_count']} time={r['duration']:.3f}s")
    assert r["final_value"] >= calculate_objective(initial)
    assert calculate_objective(r["final_state"]) == r["final_value"]
    assert is_valid(r["final_state"])