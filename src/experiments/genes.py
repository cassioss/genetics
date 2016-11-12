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

    def mutate(self, pm):
        pass


class BooleanGene(Gene):
    def __init__(self, val=False):
        Gene.__init__(self)
        self.val = val

    def __repr__(self):
        return 'BooleanGene {value: %s}' % (self.value())

    def value(self):
        return 1 if self.val else 0

    def mutate(self, pm):
        if random.random() < pm:
            self.val = coin_toss()


class RealGene(Gene):
    def __init__(self, val=0.0):
        Gene.__init__(self)
        self.val = val

    def __repr__(self):
        return 'RealGene {value: %s}' % (self.val)

    def mutate(self, pm):
        if random.random() < pm:
            self.val = random.random()


class IntegerGene(Gene):
    def __init__(self, k=2):
        if k <= 1:
            raise ValueError('IntegerGene should have a range greater than 1.')

        Gene.__init__(self)
        self.val = 0
        self.k = k

    def __repr__(self):
        return 'IntegerGene {value: %s, k: %s}' % (self.val, self.k)

    def mutate(self, pm):
        if random.random() < pm:
            self.val = random.randint(self.k)

