from data.loader import load_data
from state import State
from constraints import is_valid
from neighbors import random_neighbor, generate_neighbors
from objectives import calculate_objective

ship, vehicles = load_data("data/data.json")

for _ in range(1000):
    s = State.random(ship, vehicles)
    assert is_valid(s)

    nb = random_neighbor(s)
    if nb is not None:
        assert is_valid(nb)

s = State.random(ship, vehicles)

for p in s.placements:
    print(p.vehicle.id, p.on_ship, p.x, p.y, p.Orientation)

grid = [["." for _ in range(ship.w)] for _ in range(ship.l)]
for p in s.placements:
    for (cx, cy) in p.occupied_cells():
        grid[cy][cx] = p.vehicle.id[-1]
print("objective awal:", calculate_objective(s))
print("jumlah neighbor valid:", len(generate_neighbors(s)))
print("\n".join(" ".join(r) for r in grid))
print("neighbor:", len(generate_neighbors(s)))