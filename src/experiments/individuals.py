from genes import new_gene
from utils import arrow_list_str
from dijkstra import tsp_dist, tsp_path, tsp_full_path, dijkstra_gsize
import numpy.random as random


def new_individual(ind_name, gene_type=None, gsize=None):
    constructor = globals()[ind_name]
    if gene_type is None:
    	return constructor()
    elif gsize is None:
    	return constructor(gene_type)
    else:
    	return constructor(gene_type, gsize)


class Individual:
	def __init__(self, gene_type, gsize):
		self.gene_type = gene_type
		self.genes = [new_gene(gene_type) for x in range(gsize)]
		self.fitness = 0.0

	def __len__(self):
		return len(self.genes)

	def __repr__(self):
		return 'Individual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	@classmethod
	def from_genes(cls, gene_type, genes, gsize):
		ind = cls(gene_type, gsize)
		ind.genes = genes
		return ind


class OneMaxIndividual(Individual):
    def __init__(self, gene_type='BooleanGene', gsize=100):
        Individual.__init__(self, gene_type, gsize)

	def __repr__(self):
		return 'OneMaxIndividual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	def __str__(self):
		return str([x.value() for x in self.genes])


class TSPIndividual(Individual):
	def __init__(self, gene_type='IntegerGene', gsize=dijkstra_gsize):
		Individual.__init__(self, gene_type, gsize)
		self.gene_type = gene_type
		self.genes = [new_gene(gene_type, csize) for csize in reversed(range(2, gsize))]
		self.fitness = 0.0

	def __repr__(self):
		return 'TSPIndividual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	def __str__(self):
		sequence = [x.value() for x in self.genes]
		string =  '\nDistance       : ' + str(tsp_dist(sequence))
		string += '\nCities visited : ' + arrow_list_str(tsp_path(sequence))
		string += '\nFull path      : ' + arrow_list_str(tsp_full_path(sequence))
		return string
