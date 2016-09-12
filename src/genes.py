import numpy.random as rand


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
        return rand.randint(self.max)

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
        return self.enum[rand.randint(self.max)]

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
