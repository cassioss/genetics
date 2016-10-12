import numpy.random as random
from utils import coin_toss


def new_gene(gene_name):
    constructor = globals()[gene_name]
    return constructor()


class Gene:
    def __init__(self):
        self.val = None

    def __repr__(self):
        return 'Gene {value: %s}' % (self.val)

    def value(self):
        return self.val

    def mutate(self):
        pass

    def mate(self, gene2):
        return None


class BooleanGene(Gene):
    def __init__(self, val=False):
        Gene.__init__(self)
        self.val = val

    def __repr__(self):
        return 'BooleanGene {value: %s}' % (self.value())

    def value(self):
        return 1 if self.val else 0

    def mutate(self):
        self.val = coin_toss()

    def mate(self, gene2):
        combined = self.val if self.val is gene2.val else coin_toss()
        return BooleanGene(combined)


class RealGene(Gene):
    def __init__(self, val=0.0):
        Gene.__init__(self)
        self.val = val

    def __repr__(self):
        return 'RealGene {value: %s}' % (self.val)

    def mutate(self):
        self.val = random.random()

    def mate(self, gene2):
        cross_value = random.uniform(self.val, gene2.val)
        return RealGene(cross_value)
