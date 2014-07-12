"""
Script that visualize the browsing history
"""

from _collections import defaultdict
import datetime
import sqlite3

import matplotlib.pyplot as plt
import networkx as nx


placesPath = '../places-ct.sqlite'

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
  url_mapping = defaultdict(int, url_mapping)
  conn.close()
  return history, url_mapping



def visualize(history_list, url_mapping):
  #initialize a graph
  g = nx.Graph()

#   all_vertices_ID_with_duplicate = [ history[1] for history in history_list] + \
#                     [ history[2] for history in history_list]
#      
#   all_unique_vertices = set(all_vertices_ID_with_duplicate)
#    
#   #add all vertices into the graph
#   for node_index in list(all_unique_vertices):
#     g.add_node(url_mapping[node_index])
#  
#     all_edges = [(url_mapping[history[1]], url_mapping[history[2]],{'visit_date': history[3],\
#     'visit_type': history[4],\
#     }) for history in history_list]
#     g.add_edges_from(all_edges)
    
  
  # add all vertices into the graph
  #vertices = url_mapping.keys()
  #for node_id in vertices:
  #  g.add_node(node_id)
  
  for entry in history_list[:1000]:
    visit_date = datetime.datetime.utcfromtimestamp(entry[3] / 1000000.0)
    visit_type = entry[4]
   
    g.add_edge(entry[1], entry[2])
                #color='red',
                #visit_date=entry[3],
                #visit_type=visit_type]
                
  nx.draw(g, pos=nx.graphviz_layout(g),
          node_size=[10 * g.degree(n) for n in g.nodes()],
          node_color=range(len(g.nodes())),
          cmap=plt.cm.Blues,
          #with_labels = True,
          )
  plt.show()

def init():
  history_list, url_mapping = extract_history_records()
  visualize(history_list, url_mapping)
init()
