import random
from constraints import is_valid


def move_vehicle(state, index):
    new_state = state.copy()
    placement = new_state.placements[index]

    width, length = placement.effective_dimensions()

    if width > new_state.ship.w or length > new_state.ship.l:
        return None

    placement.on_ship = True
    placement.x = random.randint(0, new_state.ship.w - width)
    placement.y = random.randint(0, new_state.ship.l - length)

    return new_state


def change_orientation(state, index):
    if not state.placements[index].on_ship:
        return None

    new_state = state.copy()
    placement = new_state.placements[index]

    placement.Orientation = "V" if placement.Orientation == "H" else "H"

    return new_state


def swap_vehicles(state, index1, index2):
    if not state.placements[index1].on_ship and not state.placements[index2].on_ship:
        return None

    new_state = state.copy()

    p1 = new_state.placements[index1]
    p2 = new_state.placements[index2]

    p1.x, p2.x = p2.x, p1.x
    p1.y, p2.y = p2.y, p1.y
    p1.on_ship, p2.on_ship = p2.on_ship, p1.on_ship

    return new_state


def generate_move_neighbors(state, index):
    neighbors = []

    placement = state.placements[index]

    temp_placement = placement.copy()
    temp_placement.on_ship = True

    width, length = temp_placement.effective_dimensions()

    if width > state.ship.w or length > state.ship.l:
        return neighbors

    for x in range(state.ship.w - width + 1):
        for y in range(state.ship.l - length + 1):

            if placement.on_ship and placement.x == x and placement.y == y:
                continue

            new_state = state.copy()
            new_placement = new_state.placements[index]

            new_placement.on_ship = True
            new_placement.x = x
            new_placement.y = y

            if is_valid(new_state):
                neighbors.append(new_state)

    return neighbors


def generate_neighbors(state):
    neighbors = []

    num_vehicles = len(state.placements)

    for i in range(num_vehicles):
        neighbors.extend(generate_move_neighbors(state, i))

    for i in range(num_vehicles):
        neighbor = change_orientation(state, i)

        if neighbor is not None and is_valid(neighbor):
            neighbors.append(neighbor)

    for i in range(num_vehicles):
        for j in range(i + 1, num_vehicles):
            neighbor = swap_vehicles(state, i, j)

            if neighbor is not None and is_valid(neighbor):
                neighbors.append(neighbor)

    return neighbors

def random_neighbor(state, max_tries=50):
    n = len(state.placements)

    for _ in range(max_tries):
        r = random.random()

        if r < 0.4:
            new = move_vehicle(state, random.randrange(n))
        elif r < 0.6:
            new = change_orientation(state, random.randrange(n))
        else:
            if n < 2:
                continue
            i, j = random.sample(range(n), 2)
            new = swap_vehicles(state, i, j)

        if new is not None and is_valid(new):
            return new

    return None 