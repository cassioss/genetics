import numpy.random as random

def nonzero_rand(limit):
	return random.randint(limit + 1)

# Gets two distinct random positions in a list of  
def crossover_two_point(ind1, ind2):
	if len(ind1) < 2 or len(ind1) != len(ind2):
		return

	length = len(ind1)

	if length == 2:
		return ind1[:1] + ind2[1:], ind2[:1] + ind1[1:]

	rand1 = nonzero_rand(length)
	rand2 = nonzero_rand(length)

	while (rand1 == rand2) or (rand1 == 0 and rand2 == length) or (rand2 == 0 and rand1 == length):
		rand2 = nonzero_rand(length)

	rand1, rand2 = (rand1, rand2) if rand1 < rand2 else (rand2, rand1)

	one_crossed = ind1[:rand1] + ind2[rand1:rand2] + ind1[rand2:]
	two_crossed = ind2[:rand1] + ind1[rand1:rand2] + ind2[rand2:]

	if one_crossed == ind1 or two_crossed == ind1:
		print rand1, rand2
		raise ValueError('Error')

	return one_crossed, two_crossed

for i in range(2000):
	print crossover_two_point([0,1,1,0,0,0], [1,0,0,1,1,1])