def check_within_ship(placement, ship):
    if not placement.on_ship:
        return True

    width, length = placement.effective_dimensions()

    return (
        placement.x >= 0
        and placement.y >= 0
        and placement.x + width <= ship.w
        and placement.y + length <= ship.l
    )


def check_overlap(state):
    all_cells = set() 

    for placement in state.placements:
        for cell in placement.occupied_cells():

            if cell in all_cells:
                return False

            all_cells.add(cell)

    return True


def check_capacity(state):
    total_weight = 0

    for placement in state.placements:
        if placement.on_ship:
            total_weight += placement.vehicle.Weight

    return total_weight <= state.ship.MaxCapacity

def is_valid(state):
    for placement in state.placements:
        if not check_within_ship(placement, state.ship):
            return False

    if not check_overlap(state):
        return False

    if not check_capacity(state):
        return False

    return True