import numpy.random as random
import copy

def new_object(class_id):
    constructor = globals()[class_id]
    return constructor()

def onemax_fitness(population):
    return sum(gene.value() for gene in population)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def sum2(numbers):
    return sum(x*x for x in numbers)

def std(numbers):
    length = len(numbers)
    avg = mean(numbers)
    sum_sum = sum2(numbers)
    return abs(sum_sum/length - avg**2)**0.5

class Gene:
    def __init__(self):
        self.fitness = 0.0
        self.val = None

    def __str__(self):
        pass

    def value(self):
        pass

    # Helper function for random boolean
    # Numpy's random() iterates over [0,1), so a fair distribution would be between [0, 0.5) and [0.5, 1)
    @staticmethod
    def coin_toss():
        return random.random() >= 0.5


class BooleanGene(Gene):
    def __init__(self, val=False):
        Gene.__init__(self)
        self.val = val

    def __str__(self):
        return str(self.value())

    def value(self):
        return 1 if self.val else 0

    def mutate(self):
        self.val = self.coin_toss()

    def mate(self, gene2):
        child1 = BooleanGene(self.val)
        child2 = BooleanGene(gene2.val)
        return child1, child2


class RealGene(Gene):
    def __init__(self, val=0.0):
        Gene.__init__(self)
        self.val = val

    def __str__(self):
        return str(self.val)

    def value(self):
        return self.val

    def mutate(self):
        self.val = random.random()

    def mate(self, gene2):
        cross_value = random.uniform(self.val, gene2.val)
        child1 = RealGene(cross_value)
        child2 = RealGene(self.val + gene2.val - cross_value)
        return child1, child2


class GeneFlow:
    def __init__(self, gene_type, ffit=None, pm=0.01, pc=0.7, mu=100, ngen=20):
        self.fitness = ffit
        self.population = [new_object(gene_type) for x in range(mu)]
        self.pm = pm
        self.pc = pc
        self.mu = mu
        self.ngen = ngen

    def gene_str(self, genes):
        genes.sort(key=lambda gene:gene.value(), reverse=True)
        return [gene.value() for gene in genes]

    def population_str(self):
        return self.gene_str(self.population)

    def stats(self):
        print('Population: %s' % self.population_str())
        print('Fitness: %.6f' % self.fitness(self.population))
        print('Min    : %.6f' % min([x.value() for x in self.population]))
        print('Max    : %.6f' % max([x.value() for x in self.population]))
        print('Average: %.6f' % mean([x.value() for x in self.population]))
        print('Std    : %.6f' % std([x.value() for x in self.population]))

    def generate(self):
        print('Generation 0:')
        self.stats()

        for i in range(self.ngen):
            print('\nGeneration %s:' % (i+1))
            self.update()
            self.stats()

    def update(self):
        self.select()
        self.crossover()
        self.mutate()
        self.replace()
        pass

    # The population is selected to be crossed randomly
    def select(self):
        random.shuffle(self.population)
        self.offspring = [None for x in range(len(self.population))]

        # print('Population: %s' % self.population_str())
        # print('Selection : %s' % self.gene_str(self.offspring))

    # Genes are crossed over with probability pc
    def crossover(self):
        for i in range(0, len(self.offspring), 2):
            for j in range(1, len(self.offspring), 2):
                if random.random() < self.pc:
                    child1, child2 = self.mate(self.population[i], self.population[j])
                    self.offspring[i] = child1
                    self.offspring[j] = child2

        # print('X-over    : %s' % self.gene_str(self.offspring))

    # Two genes are crossed over, generating two new genes
    def mate(self, ind1, ind2):
        return ind1.mate(ind2)

    # Mutation only acts over the offspring, with probability pm
    def mutate(self):
        for gene in self.offspring:
            if random.random() < self.pm:
                gene.mutate()

        # print('Mutation  : %s' % self.gene_str(self.offspring))

    # Only the best members survive
    def replace(self):
        self.population = self.population + self.offspring
        self.population.sort(key=lambda gene:gene.value(), reverse=True)
        self.population = self.population[:self.mu]


# GeneFlow('BooleanGene', onemax_fitness).generate()
GeneFlow('RealGene', onemax_fitness).generate()
