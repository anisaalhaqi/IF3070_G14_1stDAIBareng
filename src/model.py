class Vehicle:
    def __init__(self, id, w, l, ShippingFee, Weight, ETA):
        self.id = id
        self.w = w
        self.l = l
        self.ShippingFee = ShippingFee
        self.Weight = Weight
        self.ETA = ETA

    def dimensi(self):
        return self.w, self.l

    def __repr__(self):
        return (
            f"Vehicle("
            f"id={self.id}, "
            f"w={self.w}, "
            f"l={self.l}, "
            f"ShippingFee={self.ShippingFee}, "
            f"Weight={self.Weight}, "
            f"ETA={self.ETA})"
        )


class Ship:
    def __init__(self, w, l, MaxCapacity):
        self.w = w
        self.l = l
        self.MaxCapacity = MaxCapacity

    def dimensi(self):
        return self.w, self.l

    def __repr__(self):
        return (
            f"Ship("
            f"w={self.w}, "
            f"l={self.l}, "
            f"MaxCapacity={self.MaxCapacity})"
        )