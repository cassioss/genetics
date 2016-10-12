from genes import new_gene


def new_individual(ind_name, gene_type, gsize=100):
    constructor = globals()[ind_name]
    return constructor(gene_type, gsize)


class Individual:
	def __init__(self, gene_type, gsize=100):
		self.gene_type = gene_type
		self.genes = [new_gene(gene_type) for x in range(gsize)]

	def __len__(self):
		return len(self.genes)

	def __repr__(self):
		return 'Individual {Gene: %s, Count: %d}' % (self.gene_type, len(self))

	@classmethod
	def from_genes(cls, gene_type, genes):
		ind = cls(gene_type)
		ind.genes = genes
		return ind

	def mate(self, other_ind):
		if self.gene_type != other_ind.gene_type:
			raise ValueError('Tried to mate two individuals with different genes')

		if len(self) != len(other_ind):
			raise ValueError('Tried to mate individuals with different gene count')

		new_genes = []
		for gene1, gene2 in zip(self.genes, other_ind.genes):
			new_genes.append(gene1.mate(gene2))

		return self.from_genes(self.gene_type, new_genes)


class OneMaxIndividual(Individual):
    def __init__(self, gene_type='BooleanGene', gsize=100):
        Individual.__init__(self, gene_type, gsize)

	def __repr__(self):
		return 'OneMaxIndividual {Gene: %s, Count: %d}' % (self.gene_type, len(self))
