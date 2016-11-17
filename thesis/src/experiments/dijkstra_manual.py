
# City map - only contains the paths between the cities

dijkstra_map = [
	('A', 'B', 12),
	('A', 'C', 20),
	('A', 'D', 25),
	('A', 'E', 15),
	('B', 'C', 40),
	('B', 'E', 17),
	('C', 'F', 12),
	('D', 'E', 30),
	('D', 'F', 40),
	('E', 'G', 10),
	('F', 'G', 10)
]

# Functions to find the graph

def create_graph(dijk_map):
	if dijk_map is None or len(dijk_map) is 0:
		return None

	graph = {}

	for edge_tuple in dijk_map:
		first_city = edge_tuple[0]
		second_city = edge_tuple[1]
		distance = edge_tuple[2]

		if graph.get(first_city) is None:
			graph[first_city] = {}

		if graph.get(second_city) is None:
			graph[second_city] = {}

		graph[first_city][second_city] = distance
		graph[second_city][first_city] = distance

	return graph

dijkstra_manual_graph = create_graph(dijkstra_map)
