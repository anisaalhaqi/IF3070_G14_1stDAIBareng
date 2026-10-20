import json
from model import Ship, Vehicle


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    s = data["ship"]
    ship = Ship(s["w"], s["l"], s["MaxCapacity"])

    vehicles = [
        Vehicle(
            v["id"], v["w"], v["l"],
            v["ShippingFee"], v["Weight"], v["ETA"]
        )
        for v in data["vehicles"]
    ]

    return ship, vehicles