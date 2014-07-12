"""
Script that visualize the browsing history
"""

from igraph import *

def visualize(history_list):
	#initialize a graph
	g = Graph()
	
	
	all_vertices_ID_with_duplicate = [ history[1] for history in history_list] + \
										[ history[2] for history in history_list]
	all_unique_vertices = set(all_vertices_ID_with_duplicate)
	num_nodes = len(all_unique_vertices)

	#add all vertices into the graph
	g.add_vertices(num_nodes)

	all_edges = [(history[1], history[2]) for history in history_list]
	g.add_edges(all_edges)


