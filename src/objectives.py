def calculate_objective(state):
    total = 0

    for placement in state.placements:
        if placement.on_ship:
            total += placement.vehicle.ShippingFee

    return total