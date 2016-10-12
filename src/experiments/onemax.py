import numpy.random as random
import fitness
from utils import *
from genes import *

class GeneFlow:
    def __init__(self, gene_type, ffit=None, pm=0.01, pc=0.7, mu=100, ngen=20):
        self.fitness = ffit
        self.population = [new_gene(gene_type) for x in range(mu)]
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
GeneFlow('RealGene', fitness.onemax).generate()
