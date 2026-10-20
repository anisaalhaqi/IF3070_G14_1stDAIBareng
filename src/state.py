import random

class Placement:
    def __init__(
        self,
        vehicle,
        Orientation="H",
        x=None,
        y=None,
        on_ship=False
    ):
        self.vehicle = vehicle
        self.Orientation = Orientation
        self.x = x
        self.y = y
        self.on_ship = on_ship

    def effective_dimensions(self):
        if self.Orientation == "V":
            return self.vehicle.l, self.vehicle.w

        return self.vehicle.w, self.vehicle.l

    def occupied_cells(self):
        if not self.on_ship:
            return []

        width, length = self.effective_dimensions()

        cells = []

        for dx in range(width):
            for dy in range(length):
                cells.append((self.x + dx, self.y + dy))

        return cells

    def copy(self):
        return Placement(
            self.vehicle,
            self.Orientation,
            self.x,
            self.y,
            self.on_ship
        )


class State:
    def __init__(self, ship, placements):
        self.ship = ship
        self.placements = placements

    def copy(self):
        return State(
            self.ship,
            [p.copy() for p in self.placements]
        )

    @classmethod
    def random(cls, ship, vehicles, tries=20):
        from constraints import is_valid

        placements = [
            Placement(v, random.choice(["H", "V"])) for v in vehicles
        ]
        state = cls(ship, placements)

        order = list(range(len(vehicles)))
        random.shuffle(order)

        for i in order:
            p = state.placements[i]
            width, length = p.effective_dimensions()

            if width > ship.w or length > ship.l:
                continue 

            for _ in range(tries):
                p.on_ship = True
                p.x = random.randint(0, ship.w - width)
                p.y = random.randint(0, ship.l - length)

                if is_valid(state):
                    break

                p.on_ship, p.x, p.y = False, None, None

        return state