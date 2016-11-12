import numpy.random as random
import fitness
from utils import *
from individuals import new_individual
from individuals import Individual

class GeneFlow:
    def __init__(self, ind_type, gene_type, ffit=None, pm=0.01, pc=0.9, mu=10, ngen=400, print_stats=True):
        self.fitness = ffit
        self.population = [new_individual(ind_type, gene_type) for x in range(mu)]
        self.pm = pm
        self.pc = pc
        self.mu = mu
        self.ngen = ngen
        self.print_stats = print_stats

    def calculate_fitness(self):
        for individual in self.population:
            individual.fitness = self.fitness(individual)

    def avg_fitness(self):
        return mean([x.fitness for x in self.population])

    def stats(self):
        if self.print_stats is False:
            return

        print('Min    : %.6f' % min([x.fitness for x in self.population]))
        print('Max    : %.6f' % max([x.fitness for x in self.population]))
        print('Average: %.6f' % mean([x.fitness for x in self.population]))
        print('Std    : %.6f' % std([x.fitness for x in self.population]))

    def generate(self):
        if self.print_stats:
            print('Generation 0:')

        self.stats()

        for i in range(self.ngen):
            if self.print_stats:
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
        self.offspring = []

    # Genes are crossed over with probability pc
    def crossover(self):
        for parent1, parent2 in zip(self.population[::2], self.population[1::2]):
            if random.random() < self.pc:
                child1, child2 = self.cross(parent1, parent2)
                self.offspring.append(child1)
                self.offspring.append(child2)

        self.population = self.population + self.offspring
        self.offspring = []
        self.calculate_fitness()

    # Two-point crossover - generates two individuals
    def cross(self, ind1, ind2):
        length = len(ind1)
        gene_type = ind1.gene_type

        genes1 = list(ind1.genes)
        genes2 = list(ind2.genes)

        rand1 = random.randint(length + 1)
        rand2 = random.randint(length + 1)

        while (rand1 == rand2) or (rand1 == 0 and rand2 == length) or (rand2 == 0 and rand1 == length):
            rand2 = random.randint(length + 1)

        rand1, rand2 = (rand1, rand2) if rand1 < rand2 else (rand2, rand1)

        one_crossed = Individual.from_genes(gene_type, genes1[:rand1] + genes2[rand1:rand2] + genes1[rand2:])
        two_crossed = Individual.from_genes(gene_type, genes2[:rand1] + genes1[rand1:rand2] + genes2[rand2:])

        return one_crossed, two_crossed

    # Mutation acts over all genes, with probability pm
    def mutate(self):
        for ind in self.population:
            for gene in ind.genes:
                if random.random() < self.pm:
                    gene.mutate()

    # Only the best members survive
    def replace(self):
        self.calculate_fitness()
        self.population.sort(key=lambda ind:ind.fitness, reverse=True)
        self.population = self.population[:self.mu]


GeneFlow('OneMaxIndividual', 'BooleanGene', fitness.onemax).generate()
#GeneFlow('OneMaxIndividual', 'RealGene', fitness.onemax).generate()
