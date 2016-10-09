import numpy.random as rand


class Gene:
    def __init__(self):
        pass

    def random(self):
        pass

    # Helper function for random boolean
    # Numpy's rand() iterates over [0,1), so a fair distribution would be between [0, 0.5) and [0.5, 1)
    @staticmethod
    def coin_toss():
        return rand.random() >= 0.5


class BooleanGene(Gene):
    def __init__(self):
        Gene.__init__(self)

    def random(self):
        return self.coin_toss()

    # Walking would simply be a change of value for a boolean
    @staticmethod
    def walk(val):
        return not val


class GeneFlow:
    def __init__(self):
        pass

    def select(self, parents):
        pass
