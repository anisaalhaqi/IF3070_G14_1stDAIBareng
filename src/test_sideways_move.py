import random

from data.loader import load_data
from state import State
from constraints import is_valid
from algorithms.sideways_move import hill_climbing_sideways
from objectives import calculate_objective

ship, vehicles = load_data("data/data.json")

for seed in (1, 2, 3):
    random.seed(seed)
    initial = State.random(ship, vehicles)
    r = hill_climbing_sideways(initial)
    print(f"seed={seed} initial={calculate_objective(initial)} "
          f"final={r['final_value']} iter={r['iterations']} "
          f"sideways={r['sideways_moves']} stop={r['stop_reason']} "
          f"time={r['duration']:.3f}s")

    assert is_valid(r["final_state"])
    assert r["final_value"] >= calculate_objective(initial)
    assert calculate_objective(r["final_state"]) == r["final_value"]