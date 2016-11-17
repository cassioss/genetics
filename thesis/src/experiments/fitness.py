from dijkstra import tsp_dist, all_cities
import copy

# Fitness function for OneMax
def onemax(individual):
    return sum(gene.value() for gene in individual.genes)

# Fitness function for TSP
def tsp(individual):
	return tsp_dist([gene.value() for gene in individual.genes])
