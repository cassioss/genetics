import numpy.random as random
import fitness
import copy
import os
from utils import *
from individuals import new_individual, from_genes
from individuals import Individual

class GeneFlow:
    def __init__(self, ind_type, gene_type, ffit=None, pc=0.9, pm=0.01, mu=100, ngen=200,
                print_stats=True, maximum=True, elitism=True, adaptive=False):
        self.fitness = ffit
        self.population = [new_individual(ind_type, gene_type) for x in range(mu)]
        self.pm = pm
        self.pm0 = pm
        self.pc = pc
        self.mu = mu
        self.ngen = ngen
        self.print_stats = print_stats
        self.maximum = maximum
        self.elitism = elitism
        self.adaptive = adaptive
        self.start_writing(ind_type, gene_type)


    def start_writing(self, ind_type, gene_type):
        file_name = '../out/' + ind_type + '_' + gene_type + ('' if not self.adaptive else '_adaptive')
        new_path = os.path.relpath(file_name + '.csv', os.path.dirname(__file__))
        self.file = open(new_path, 'w')
        self.file.write('Generation,Min,Max,Avg,Std\n')

        if self.adaptive:
            new_path = os.path.relpath(file_name + '_pm.csv', os.path.dirname(__file__))
            self.adapt_file = open(new_path, 'w')
            self.adapt_file.write('Generation,pm,pm0,deviation,best_fitness\n')


    def calculate_all_fitness(self):
        self.parent_fitness()
        self.offspring_fitness()

    def parent_fitness(self):
        for individual in self.population:
            individual.fitness = self.fitness(individual)

    def offspring_fitness(self):
        for individual in self.offspring:
            individual.fitness = self.fitness(individual)

    def min_fitness(self):
        return min([x.fitness for x in self.population])

    def max_fitness(self):
        return max([x.fitness for x in self.population])

    def best_fitness(self):
        return self.max_fitness() if self.maximum else self.min_fitness()

    def avg_fitness(self):
        return mean([x.fitness for x in self.population])

    def std_fitness(self):
        return std([x.fitness for x in self.population])

    def stats(self):
        if self.print_stats is False:
            return

        print('Min    : %.6f' % self.min_fitness())
        print('Max    : %.6f' % self.max_fitness())
        print('Average: %.6f' % self.avg_fitness())
        print('Std    : %.6f' % self.std_fitness())
        print('Best individual is: ' + str(self.population[0]))

    def generate(self):
        if self.print_stats:
            print('Generation 0:')

        self.parent_fitness()
        self.stats()
        self.write_to_file(0)

        for i in range(self.ngen):
            if self.print_stats:
                print('\nGeneration %s:' % (i+1))
            self.update()
            self.stats()
            self.write_to_file(i+1)

    def update(self):
        self.selection()
        self.crossover()
        self.mutation()
        self.survival()
        pass

    # The offspring is selected based on the best fitness values
    def selection(self):
        self.population.sort(key=lambda ind:ind.fitness, reverse=self.maximum)
        self.offspring = []

    # Offspring is paired and crossed over with probability pc - two parents generate two children
    def crossover(self):
        for parent1, parent2 in zip(self.population[::2], self.population[1::2]):
            if random.random() < self.pc:
                child1, child2 = self.cross(parent1, parent2)
                self.offspring.append(child1)
                self.offspring.append(child2)

    # Two-point crossover - two children mix their genes, based in a two-point section switch of their genes
    def cross(self, ind1, ind2):
        length = len(ind1)
        ind_type = ind1.__class__.__name__
        gene_type = ind1.gene_type

        genes1 = copy.deepcopy(ind1.genes)
        genes2 = copy.deepcopy(ind2.genes)

        # Two distinct points are chosen
        rand1 = random.randint(length + 1)
        rand2 = random.randint(length + 1)

        while (rand1 == rand2) or (rand1 == 0 and rand2 == length) or (rand2 == 0 and rand1 == length):
            rand2 = random.randint(length + 1)

        rand1, rand2 = (rand1, rand2) if rand1 < rand2 else (rand2, rand1)
        genes1[rand1:rand2], genes2[rand1:rand2] = genes2[rand1:rand2], genes1[rand1:rand2]

        return from_genes(ind_type, genes1, gene_type), from_genes(ind_type, genes2, gene_type)

    # Mutation acts over all genes (except the elite), with probability pm
    def mutation(self):
        if self.elitism:
            self.population.sort(key=lambda ind:ind.fitness, reverse=self.maximum)
            self.elite = copy.deepcopy(self.population[0])
            self.population = self.population[1:]

        for ind in self.population:
            for gene in ind.genes:
                if random.random() < self.pm:
                    gene.mutate()

        for ind in self.offspring:
            for gene in ind.genes:
                if random.random() < self.pm:
                    gene.mutate()

    # Only the best mu individuals survive
    def survival(self):
        if self.elitism:
            self.population.append(self.elite)

        self.calculate_all_fitness()
        self.population = self.population + self.offspring
        self.population.sort(key=lambda ind:ind.fitness, reverse=self.maximum)
        self.population = self.population[:self.mu]

        if self.adaptive:
            self.adapt()

    # Deviation of the best fitness to the average
    def deviation(self):
        if abs(self.avg_fitness()) < 0.0000001:
            return 0.0

        return abs((self.best_fitness() - self.avg_fitness()) / (self.avg_fitness()))

    # Adaptive Genetic Algorithm (AGA) module
    def adapt(self):

        # In order to avoid division by zero
        if abs(self.avg_fitness()) < 0.0000001:
            return

        # Increment pm if the deviation is lower than pm0
        if self.deviation() <= self.pm0:
            self.pm = min(0.5, self.pm + 0.001)

        # Decrement pm, otherwise
        else:
            self.pm = max(0.001, self.pm - 0.001)

        if self.print_stats:
            print self.deviation(), self.pm, self.pm0, self.best_fitness()

    def write_to_file(self, n):
        self.file.write(str(n))
        self.file.write(',')
        self.file.write(str(self.min_fitness()))
        self.file.write(',')
        self.file.write(str(self.max_fitness()))
        self.file.write(',')
        self.file.write(str(self.avg_fitness()))
        self.file.write(',')
        self.file.write(str(self.std_fitness()))
        self.file.write('\n')

        if self.adaptive:
            self.adapt_file.write(str(n))
            self.adapt_file.write(',')
            self.adapt_file.write(str(self.pm))
            self.adapt_file.write(',')
            self.adapt_file.write(str(self.pm0))
            self.adapt_file.write(',')
            self.adapt_file.write(str(self.deviation()))
            self.adapt_file.write(',')
            self.adapt_file.write(str(self.best_fitness()))
            self.adapt_file.write('\n')

# Uncomment one of the next three lines to simulate the algorithm

GeneFlow('OneMaxIndividual', 'BooleanGene', fitness.onemax, adaptive=True, print_stats=True, pm=0.01).generate()
#GeneFlow('OneMaxIndividual', 'RealGene', fitness.onemax, adaptive=True, print_stats=True, pm=0.05).generate()
#GeneFlow('TSPIndividual', 'IntegerGene', fitness.tsp, maximum=False, adaptive=True, print_stats=True, pm=0.2).generate()



