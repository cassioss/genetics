from matplotlib import pyplot
from geneflow import *

genestructure=[RealGene(-10.0,10.0),RealGene(-10.0,10.0)]

def ffunc(x):
    return (x[0]+3.0)**2+(x[1]-7.0)**2

#gflow=Optimizer(ffunc, genestructure,mutation=0.3,elitism=0.05,geostructure=[5],blending=1.0)

gflow=Optimizer(ffunc,genestructure,[3,3,3],mutation=0.001,elitism=0.5,blending=0.05,
                            walking=0.2,conserve=0.001)


vals=[]
wals=[]

pyplot.figure()

for i in range(500):
    gflow.iterate()
    data=np.transpose(np.array(gflow.population))
    pyplot.ion()
    pyplot.hold(False)
    pyplot.plot(data[0],data[1])
    pyplot.axis([-10,10,-10,10])
    pyplot.show(block=False)
    pyplot.draw()
    vals.append(-gflow.solution_fitness())
    wals.append(-gflow.worst_fitness())

pyplot.ioff()
pyplot.plot(vals)
pyplot.hold(True)
pyplot.plot(wals)
pyplot.show()


print gflow.solution()

