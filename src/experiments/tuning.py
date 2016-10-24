import fitness
import numpy as np
from onemax import *

def test_tuning(NGEN=500):
	best_fitness = 0.0
	best_pc = 0.0

	for tuning_pc in np.linspace(0.8, 1., 21):
		flow = GeneFlow('OneMaxIndividual', 'RealGene', fitness.onemax, ngen=NGEN,
			print_stats=False, pc=tuning_pc)

		flow.generate()
		if best_fitness < flow.avg_fitness():
			best_fitness = flow.avg_fitness()
			best_pc = tuning_pc
	print("Best Fitness: %.6f" % best_fitness)
	print("Best pc     : %.6f" % best_pc)

	best_fitness = 0.0
	best_pm = 0.0

	for tuning_pm in np.linspace(0, 0.1, 101):
		flow = GeneFlow('OneMaxIndividual', 'RealGene', fitness.onemax, ngen=NGEN,
			print_stats=False, pc=best_pc, pm=tuning_pm)

		flow.generate()

		if best_fitness < flow.avg_fitness():
			best_fitness = flow.avg_fitness()
			best_pm = tuning_pm

	print("Best Fitness: %.6f" % best_fitness)
	print("Best pm     : %.6f" % best_pm)

test_tuning(1000)