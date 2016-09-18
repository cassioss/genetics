from src.geneflow import *
import numpy as np

metagstr=[EnumGene([0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])]*5+\
               [EnumGene([[3],[4],[5],[10],[3,3],[3,3,3],[4,4]])]

genestructure=[BooleanGene()]*1475

def ffit(x):
    return np.sum(x)

#~ def metafit(v):
    #~ totaltime=0
    #~ initcost=np.sum(v[5])
    #~ for r in range(10):                            
        #~ gflow=Optimizer(ffit, genestructure, mutation=v[0], elitism=v[1], walking=v[2],
                                #~ blending=v[3], conserve=v[4], geostructure=v[5], signal=-1.0)
        #~ stoptime=2000
        #~ for i in range(2000):
            #~ gflow.iterate()
            #~ if gflow.solution_fitness()>8.0:
                #~ stoptime= i
                #~ break
        #~ totaltime+=stoptime+initcost
    #~ return totaltime
 
def metafit(v):
    totalboon=0
    for r in range(10):                            
        gflow=Optimizer(ffit, genestructure, mutation=v[0], elitism=v[1], walking=v[2],
                                blending=v[3], conserve=v[4], geostructure=v[5], signal=-1.0)
        for i in range(100):
            gflow.iterate()
        totalboon+=gflow.solution_fitness()
    return totalboon
 
    
#~ metagflow=Optimizer(metafit,metagstr,[5])
metagflow=Optimizer(metafit, metagstr, mutation=0.02, elitism=0.7, walking=0.1,
                               blending=0.4, conserve=0.02, geostructure=[3,3])

for i in range(2000):
    metagflow.iterate()
    print metagflow.solution()
    print metagflow.solution_fitness()
    
print metagflow.solution()



    

