import copy
from dijkstra17 import dijkstra17_graph

# Functions that apply Dijkstra's algorithm

def dijkstra_all(graph):
	full_map = {}
	for source in graph:
		dist, prev = dijkstra(graph, source)
		full_map[source] = {}
		full_map[source]['dist'] = dist
		full_map[source]['prev'] = prev
	return full_map

def dijkstra(graph, source):
	Q = set()
	dist = {}
	prev = {}

	for vertex in graph:
		dist[vertex] = float("inf")
		prev[vertex] = None
		Q.add(vertex)

	dist[source] = 0

	while len(Q) is not 0:
		u = min_value(Q, dist)
		Q.remove(u)

		for v in graph[u]:
			alt = dist[u] + graph[u][v]
			if alt < dist[v]:
				dist[v] = alt
				prev[v] = u

	return dist, prev

def min_value(Q, dist):
	u = next(iter(Q))
	for v in Q:
		if dist[v] < dist[u]:
			u = v
	return u

# Global variables
complete_graph = dijkstra_all(dijkstra17_graph)
all_cities = [node for node in complete_graph]
all_cities.sort()

# Functions to calculate distance
def dist_between(a, b, dijkstra_graph=complete_graph):
	return dijkstra_graph[a]['dist'][b]

def tsp_dist(sequence):
	copy_cities = copy.copy(all_cities)
	init = copy_cities.pop(0)
	prev = init
	next = None
	tsp_sum = 0
	for i in sequence:
		prev = prev if next is None else next
		next = copy_cities.pop(i)
		tsp_sum += dist_between(prev, next)
	tsp_sum += dist_between(next, copy_cities[0])
	tsp_sum += dist_between(copy_cities[0], init)
	return tsp_sum

# Functions to find paths
def path_between(a, b, dijkstra_graph=complete_graph):
	path = [b]
	prev = dijkstra_graph[a]['prev'][b]
	while prev is not None:
		path.insert(0, prev)
		prev = dijkstra_graph[a]['prev'][prev]
	return path

def tsp_path(sequence):
	copy_sequence = copy.copy(sequence)
	copy_sequence.append(0)

	copy_cities = copy.copy(all_cities)
	init = copy_cities.pop(0)
	tsp_path = [init]

	for i in copy_sequence:
		tsp_path.append(copy_cities.pop(i))

	tsp_path.append(init)
	return tsp_path

def tsp_full_path(sequence):
	path = tsp_path(sequence)
	full_path = []
	for first, second in zip(path, path[1:]):
		full_path = full_path[:-1] + path_between(first, second)
	return full_path

dijkstra_gsize = len(all_cities)
