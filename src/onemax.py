from geneflow import *
import numpy as np

genestructure=[BooleanGene()]*100

def ffit(x):
    return np.sum(x)
    
#gflow=Optimizer(ffit, genestructure,mutation=0.3,elitism=0.05,walking=0,geostructure=[5],blending=1.0,signal=1.0)
#gflow=Optimizer(ffit, genestructure,mutation=0.001,elitism=0.5,walking=0.2,geostructure=[5],blending=1.0,signal=1.0)
#~ gflow=Optimizer(ffit, genestructure, mutation=0.001, elitism=0.5, walking=0.2,
                               #~ blending=0.05, conserve=0.001, geostructure=[3,3,3], signal=1.0)

gflow=Optimizer(ffit, genestructure, mutation=0.02, elitism=0.7, walking=0.1,
                               blending=0.4, conserve=0.02, geostructure=[3,3], signal=1.0)

#~ gflow=Optimizer(ffit, genestructure, mutation=0.3, elitism=0.01, walking=0.6,
                               #~ blending=0.8, conserve=0.05, geostructure=[3], signal=1.0)

#~ gflow=Optimizer(ffit, genestructure, mutation=0.001, elitism=0.7, walking=0.3,
                               #~ blending=0.7, conserve=0, geostructure=[5], signal=1.0)

for i in range(5000):
    gflow.iterate()
    print "%5d -> %s fit:%f" % (i,[1 if i else 0 for i in gflow.solution()],gflow.solution_fitness())
    
print gflow.solution_fitness()
