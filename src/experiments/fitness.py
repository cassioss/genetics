
# Fitness function for OneMax
def onemax(person):
    return sum(gene.value() for gene in person)