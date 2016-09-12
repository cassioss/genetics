import numpy as np
from matplotlib import pyplot
from geneflow import *

def sig(x):
    return 1.0/(1.0+np.exp(-x))
    
def linear(x):
    return x
    
def truncated_linear(x):
    return min(max(x,-1.0),1.0)
    
def rbf(x):
    return np.exp(-x**2) 

class Node:
    def __init__(self):
        pass
        
    def read(self):
        return 0.0

class InnerNode (Node):
    def __init__(self,inlayer, activation=sig):
        self.inlayer=inlayer
        self.w= [0.0] * len(inlayer)
        self.bias=0.0
        self.activation=activation
        
    def get_weights(self):
        return self.w+[self.bias]
        
    def set_weights(self,v):
        #assert len(v)>=len(self.w)+1
        for i in range(len(self.w)):
            self.w[i]=v.next()
        self.bias=v.next()
        
    def read(self):
        y=self.bias
        for i in range(len(self.w)):
            y+=self.w[i]*self.inlayer[i].read()
        return self.activation(y)

class OutputNode(InnerNode):
    def __init__(self,inlayer):
        self.inlayer=inlayer
        self.w= [0.0] * len(inlayer)
        self.bias=0.0
        
    def read(self):
        y=self.bias
        for i in range(len(self.w)):
            y+=self.w[i]*self.inlayer[i].read()
        return y
        
class InputNode(Node):
    def __init__(self):
        self.value=0.0
        
    def read(self):
        return self.value
        
    def feed(self,value):
        self.value=value
        
    def set_weights(self,v):
        pass
        
    def get_weights(self):
        return []
        

xnode=InputNode()

#~ inputlayer=[xnode]
#~ hidden1=[InnerNode(inputlayer,activation=sig) for i in range(8)]
#~ hidden2=[InnerNode(hidden1,activation=linear) for i in range(8)]
#~ ynode=OutputNode(hidden2)
#~ outputlayer=[ynode]

inputlayer=[xnode]
hidden1=[InnerNode(inputlayer,activation=rbf) for i in range(4)]
hidden2=[]
ynode=OutputNode(hidden1)
outputlayer=[ynode]


allnet=inputlayer+hidden1+hidden2+outputlayer

def get_vector():
    v=[a for n in allnet for a in n.get_weights()]
    return v
    
def load_vector(v):
    vv=iter(v)
    for n in allnet:
        n.set_weights(vv)        

v=get_vector()
print len(v)

genestructure=[RealGene(-50.0,50.0,step=1.0)] * len(v)
#genestructure=[FreeRealGene(step=0.5)] * len(v)

def func(x): return np.sin(x*(2.0*np.pi))**3.0

def ffit(v):
    load_vector(v)
    error=0.0
    for x in np.linspace(0.0,1.0,30):
        xnode.feed(x)
        y=ynode.read()
        error+=abs(func(x)-y)**2.0
    return error  #+0.1*np.linalg.norm(v,2)

#~ resp=[]
#~ load_vector([10.0,-5, 2,-3, 0.2,-0.5, 0.2,-0.6, 1.0, 0.3, 0.0, 0.0, 0.0])
#~ for x in np.linspace(0.0,1.0,30):
    #~ resp.append
    #~ xnode.feed(x)
    #~ resp.append(ynode.read())
    
def ffit1(v):
    load_vector(v)
    error=0.0
    for x,r in zip(np.linspace(0.0,1.0,30),resp):
        xnode.feed(x)
        y=ynode.read()
        error+=abs(r-y)**2.0
    return error   #+0.1*np.linalg.norm(v,1)

    
#gflow=Optimizer(ffit,genestructure,[3,3],mutation=0,elitism=0.25,blending=1.0,
#                            walking=0.01,conserve=0)
gflow=Optimizer(ffit,genestructure,[3,3,3],mutation=0.001,elitism=0.5,blending=0.05,
                            walking=0.2,conserve=0.001)

vals=[]

pyplot.figure()
pyplot.ion()

x=np.linspace(0.0,1.0,100)
for i in range(100000):
    gflow.iterate()
    if i%100==0:
        b=gflow.solution()
        y=[]
        s=[]
        u=[]
        for xx in x:
            xnode.feed(xx)
            y.append(ynode.read())
            s.append(func(xx))
        load_vector(b)
        for xx in x:
            xnode.feed(xx)
            u.append(ynode.read())
        pyplot.clf()
        #~ pyplot.plot(np.linspace(0.0,1.0,30),resp,'b-')
        pyplot.plot(x,s,'b:',x,u,'r-',x,y,'m-')
        pyplot.axis([-0.2,1.2,-2.0,2.0])
        pyplot.draw()
    vals.append(-gflow.solution_fitness())

pyplot.ioff()
pyplot.clf()
pyplot.plot(vals)
pyplot.show()
b=gflow.solution()
load_vector(b)
u=[]
s=[]
for xx in x:
    xnode.feed(xx)
    u.append(ynode.read())
    s.append(func(xx))
pyplot.clf()
pyplot.plot(x,s,'b:',x,u,'r-')
pyplot.show()

    


    
    