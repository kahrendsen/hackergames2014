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

  c.execute("""select * from moz_historyvisits""")

  history = c.fetchall()
  
  conn.close()
  return history

def visualize(history_list):
  # initialize a graph
  g = nx.Graph()


  all_vertices_ID_with_duplicate = [ history[1] for history in history_list] + \
                    [ history[2] for history in history_list]

  max_num_nodes = max(all_vertices_ID_with_duplicate)

  all_unique_vertices = set(all_vertices_ID_with_duplicate)
  # num_nodes = len(all_unique_vertices)

  # add all vertices into the graph
  g.add_nodes_from(list(all_unique_vertices))

  all_edges = [(history[1], history[2]) for history in history_list]
  g.add_edges_from(all_edges)

  nx.draw(g, with_labels=True)
  plt.show()

def init():
  history_list = extract_history_records()
  visualize(history_list)

init()
