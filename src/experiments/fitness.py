
# Fitness function for OneMax
def onemax(individual):
    return sum(gene.value() for gene in individual.genes)
