import numpy as np
import numpy.random as rand
import heapq


# Gene types
class Gene:
    def __init__(self):
        pass

    def random(self):
        pass

    def is_real(self):
        return False

    # Helper function for random boolean
    # Numpy's rand() iterates over [0,1), so a fair distribution would be between [0, 0.5) and [0.5, 1)
    @staticmethod
    def coin_toss():
        return rand.random() >= 0.5

    # Helper function for integer walk (moves its position by 1 in a range)
    @staticmethod
    def integer_walk(pos, max_value, direction_is_up):
        return ((pos + 1) if direction_is_up else (pos + max_value - 1)) % max_value


class BooleanGene(Gene):
    def __init__(self):
        Gene.__init__(self)

    def random(self):
        return self.coin_toss()

    # Walking would simply be a change of value for a boolean
    @staticmethod
    def walk(val):
        return not val


# An Integer Gene would be limited by a maximum value (or expressiveness)
class IntegerGene(Gene):
    def __init__(self, max_value):
        Gene.__init__(self)
        self.max = max_value

    def random(self):
        return np.random.randint(self.max)

    # Walking would be to go up or down by a unit
    def walk(self, val):
        return self.integer_walk(val, self.max, self.coin_toss())


# EnumGene would treat a list of enums similar to how the IntegerGene treats a range of integers
class EnumGene(Gene):
    def __init__(self, enum):
        Gene.__init__(self)
        assert enum
        self.enum = enum
        self.max = len(enum)

    def random(self):
        return self.enum[np.random.randint(self.max)]

    # Similar
    def walk(self, val):
        i = self.enum.index(val)
        return self.enum[self.integer_walk(i, self.max, self.coin_toss())]


class RealGene(Gene):

    # Step is 1% of the difference between min and max if not set
    def __init__(self, min_value, max_value, step=None):
        Gene.__init__(self)
        self.min = min_value
        self.max = max_value
        self.step = (self.max - self.min) * 0.01 if step is None else step

    def random(self):
        return self.min + rand.random() * (self.max - self.min)

    def is_real(self):
        return True

    def walk(self, val):
        random_step = rand.randn() * self.step
        return max(self.min, min(self.max, val + random_step))


class FreeRealGene(Gene):

    # Step here is bigger then the RealGene for a bigger (statistical) freedom
    def __init__(self, step=None):
        Gene.__init__(self)
        self.step = 0.1 if step is None else step

    def random(self):
        return rand.randn()

    def is_real(self):
        return True

    def walk(self, val):
        random_step = rand.randn() * self.step
        return val + random_step


# Object for heaps
class IndexedValue:
    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value >= other.value

    def __lt__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value


# Utilities
def quad_from_pts(x1, x2, x3, y1, y2, y3):
    """
    returns (a,b,c) for y=a*x**2+b*x+c
    """
    s1 = x1 - x2
    s2 = x1 - x3
    s3 = x2 - x3
    d1 = s1 * s2
    d2 = -s2 * s3
    d3 = s1 * s2
    if d1 == 0.0: raise FloatingPointError
    if d2 == 0.0: raise FloatingPointError
    if d3 == 0.0: raise FloatingPointError
    f1 = y1 / d1
    f2 = y2 / d2
    f3 = y3 / d3
    a = f1 + f2 + f3
    b = -f1 * (x2 + x3) - f2 * (x1 + x3) - f3 * (x1 + x2)
    c = f1 * x2 * x3 + f2 * x1 * x3 + f3 * x1 * x2
    return (a, b, c)


def minquad(x1, x2, x3, y1, y2, y3):
    """
    returns the x for estimated minimum y using quadractic polynomial
    """
    try:
        a, b, c = quad_from_pts(x1, x2, x3, y1, y2, y3)
    except:
        a = 0.0
    if a > 0.0001:
        return -b / (2.0 * a)
    elif y1 < y2 and y1 < y3:
        return x1
    elif y2 < y3:
        return x2
    else:
        return x3


# algorithm
class Optimizer:
    def __init__(self, fitness, genestructure, geostructure=[3, 3], mutation=0.05,
                 elitism=0.2, walking=0.5, conserve=0.8, signal=-1.0, blending=0.5):
        """
        initializes a geneflow algorithm.
        @fitness is a function that receives a chromossome and returns a real
        @param genestructure is a list of Gene objects of the corresponding gene type
        @param geostructure is a list of dimensions, for example [3,2,2] is a 3x2x2 world
        @param mutation chance a gene will mutate
        @param elitism chance a gene will be copied from the leader
        @param signal default -1.0 is minimization, +1.0 is maximization
        The algorithm will try to find the chromossome that optimizes the fitness
        """
        self.gstr = genestructure
        self.geo = geostructure
        self.fit = fitness
        self.signal = signal
        n_loci = len(genestructure)
        n_sites = np.prod(geostructure)
        self.elitism = elitism
        self.mutation = mutation
        self.blending = blending
        self.walking = walking
        self.conserve = conserve
        self.operation_roulette = np.cumsum([mutation, walking, elitism])
        self.population = [[x.random() for x in genestructure] for y in range(n_sites)]
        neighbors = [[]] * n_sites
        cp = np.cumprod(geostructure)
        cp[-1] = 1
        for d in cp:
            for i in range(n_sites):
                neighbors[i].append((i + d) % n_sites)
                neighbors[i].append((i + n_sites - d) % n_sites)
        self.n_sites = n_sites
        self.n_loci = n_loci
        self.neighbors = neighbors
        self.fitness = [0.0] * n_sites
        self.fitnessheap = []
        for i in range(n_sites):
            self.fitness[i] = self.signal * self.fit(self.population[i])
            self.fitnessheap.append(IndexedValue(i, self.fitness[i]))
        heapq.heapify(self.fitnessheap)

    def iterate(self):
        """
        advances the algorithm by one search step
        """
        # find and remove worst site
        worst = heapq.heappop(self.fitnessheap)
        best = heapq.nlargest(1, self.fitnessheap)[0]
        # obtain new genes from geneflow
        i = worst.index
        for g in range(self.n_loci):
            if np.random.rand() < self.conserve:
                continue
            if np.random.rand() < self.operation_roulette[0]:  # mutation
                self.population[i][g] = self.gstr[g].random()
            elif np.random.rand() < self.operation_roulette[1]:  # walking
                self.population[i][g] = self.gstr[g].walk(self.population[i][g])
            elif np.random.rand() < self.operation_roulette[2]:  # elitism
                self.population[i][g] = self.population[best.index][g]
            else:  # geneflow
                r = np.random.randint(len(self.neighbors[i]))
                r_ind = self.neighbors[i][r]
                if self.gstr[g].is_real() and np.random.rand() < self.blending:
                    # a=np.random.rand()*1.5
                    # self.population[i][g]=(1-a)*self.population[i][g]+a*self.population[r_ind][g]
                    x1, y1 = self.population[i][g], worst.value
                    x2, y2 = self.population[best.index][g], best.value
                    x3, y3 = self.population[r_ind][g], self.fitness[r_ind]
                    self.population[i][g] = minquad(x1, x2, x3, y1, y2, y3)
                else:
                    self.population[i][g] = self.population[r_ind][g]
        # recompute fitness
        worst.value = self.fitness[i] = self.signal * self.fit(self.population[i])
        # put it back in place, maybe it is no longer the worst
        heapq.heappush(self.fitnessheap, worst)

    def solution(self):
        """
        returns the best chromossome so far
        """
        best = heapq.nlargest(1, self.fitnessheap)[0]
        return self.population[best.index]

    def solution_fitness(self):
        """
        returns the fitness of the best chromossome so far
        """
        best = heapq.nlargest(1, self.fitnessheap)[0]
        return best.value

    def worst_fitness(self):
        """
        returns the fitness of the worst chromossome of the population
        """
        worst = self.fitnessheap[0]
        return worst.value
