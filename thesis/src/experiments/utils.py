import numpy.random as random

# Boolean variable on 50% chance
def coin_toss():
	return random.random() >= 0.5

# Mean value between numbers
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

# Sum of squares
def sum2(numbers):
    return sum(x*x for x in numbers)

# Standard deviation
def std(numbers):
    n = len(numbers)
    sum_sum = sum2(numbers)
    avg = mean(numbers)
    return abs((sum_sum - n*avg*avg) / (n - 1.0)) ** 0.5

# Adds arrows between values of a list
def arrow_list_str(some_list):
	return str(some_list).replace(', ', ' -> ').replace('[', '').replace(']', '').replace("'", '')