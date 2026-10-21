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

class Ship:
    def __init__(self, w, l, MaxCapacity):
        self.w = w
        self.l = l
        self.MaxCapacity = MaxCapacity

    def dimensi(self):
        return self.w, self.l