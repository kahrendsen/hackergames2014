"""
Script that visualize the browsing history
"""

import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

placesPath = '../places.sqlite'

def extract_history_records():
  conn = sqlite3.connect(placesPath)

  c = conn.cursor()

  c.execute('select sqlite_version()')

  query_text = """select moz_historyvisits.id, moz_historyvisits.from_visit, \
									moz_historyvisits.place_id,\
									moz_historyvisits.visit_date, moz_historyvisits.visit_type,\
									 moz_places.url, moz_places.title from moz_historyvisits,\
									 moz_places where moz_places.id=moz_historyvisits.place_id;
								"""
  c.execute(query_text)
  history = c.fetchall()

  url_mapping_query = """select id, url from moz_places"""
  c.execute(url_mapping_query)
  urls = c.fetchall()
  url_mapping = dict(urls)  
  url_mapping[0] = 'first_search'
  conn.close()
  return history



def visualize(history_list, url_mapping):
	#initialize a graph
	g = nx.Graph()

	all_vertices_ID_with_duplicate = [ history[1] for history in history_list] + \
										[ history[2] for history in history_list]
		
	all_unique_vertices = set(all_vertices_ID_with_duplicate)
	
	#add all vertices into the graph
	for node_index in list(all_unique_vertices):
		g.add_node(url_mapping[node_index])

	all_edges = [(url_mapping[history[1]], url_mapping[history[2]],{'visit_date': history[3],\
																				'visit_type': history[4],\
                                        }) for history in history_list]
  	g.add_edges_from(all_edges)
  	nx.draw(g, with_labels = True)
  	plt.show()

def init():
	history_list, url_mapping = extract_history_records()
	visualize(history_list, url_mapping)
init()
