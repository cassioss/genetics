from src.geneflow import *

queens=8

genestructure = [IntegerGene(queens)]*queens

def ffit(x):
    penality=0.0
    for i in range(queens):
        for j in range(i):
            #number of queens on same column
            if x[i]==x[j]:
                penality=penality+1
            #number of queens on same diagonal
            if (x[i]-i)==(x[j]-j):
                penality=penality+1
            if (x[i]+i)==(x[j]+j):
                penality=penality+1
    return penality

#gflow=Optimizer(ffunc,genestructure,geostructure=[4,4],mutation=0.1,elitism=0.1)
#~ gflow=Optimizer(ffit, genestructure, mutation=0.02, elitism=0.02, walking=0.2,
                        #~ blending=0.05, conserve=0.02, geostructure=[5], signal=-1.0)
gflow=Optimizer(ffit, genestructure, mutation=0.1, elitism=0.2, walking=0.01,
                        blending=1.0, conserve=0.6, geostructure=[4], signal=-1.0)


for i in range(500):
    gflow.iterate()
    
sol=gflow.solution()
for p in sol:
    print "O "*p+"* "+"O "*(queens-p-1)
    
print gflow.solution_fitness()
