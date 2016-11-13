from genes import new_gene
import numpy.random as random


def new_individual(ind_name, gene_type, gsize=100):
    constructor = globals()[ind_name]
    return constructor(gene_type, gsize)


class Individual:
	def __init__(self, gene_type, gsize=100):
		self.gene_type = gene_type
		self.genes = [new_gene(gene_type) for x in range(gsize)]
		self.fitness = 0.0

	def __len__(self):
		return len(self.genes)

	def __repr__(self):
		return 'Individual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	@classmethod
	def from_genes(cls, gene_type, genes):
		ind = cls(gene_type)
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
	def __init__(self, gene_type='IntegerGene', cities=6):
		self.gene_type = gene_type
		self.genes = [new_gene(gene_type, csize) for csize in range(2, cities)]
		self.fitness = 0.0

	def __repr__(self):
		return 'TSPIndividual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	def __str__(self):
		return str([(x.value(), x.k) for x in self.genes])
