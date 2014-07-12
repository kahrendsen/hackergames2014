"""
Script that visualize the browsing history
"""

from _collections import defaultdict
import argparse
import datetime
import math
import sqlite3
import sys

import matplotlib.pyplot as plt
import networkx as nx
import urllib
import webbrowser


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



def visualize(history_list, url_mapping, layoutMethod):
  # initialize a graph
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
  # vertices = url_mapping.keys()
  # for node_id in vertices:
  #  g.add_node(node_id)

  #colorMap = {}
  
  for entry in history_list[:1000]:
    visit_date = datetime.datetime.utcfromtimestamp(entry[3] / 1000000.0)
    visit_type = entry[4]
   
    color = ''
    if visit_type == 1:
      color = 'r'
    elif visit_type == 2:
      color = 'b'
    elif visit_type == 3:
      color = 'g'
    elif visit_type == 4:
      color = "black"
    g.add_edge(entry[1], entry[2], color=color)
                # color='red',
                # visit_date=entry[3],
                # visit_type=visit_type]
    #colorMap += color
  
  
  labelsMap = {}
  for n in g.nodes():
    if g.degree(n) > 5:
      labelsMap[n] = url_mapping[n]
    else:
      labelsMap[n] = ''
  
#   layout = nx.circular_layout(g)
#   
#   if layoutMethod == '--circular':
#     layout = nx.circular_layout(g)
#   elif layoutMethod == '--shell':
#     layout = nx.shell_layout(g)
#     print 'shell'
#   elif layoutMethod == '--graphviz':
#     layout = nx.graphviz_layout(g)
#   elif layoutMethod == '--fruchterman':
#     layout = nx.fruchterman_reingold_layout(g)
#   elif layoutMethod == '--random':
#     layout = nx.random_layout(g)
#   elif layoutMethod == '--spring':
#     layout = nx.spring_layout(g)
#   elif layoutMethod == '--spectral':
#     layout = nx.spectral_layout(g)
  
  layout = layoutMethod(g)
  nx.draw(g, pos=layout,
          node_size=[20 * g.degree(n) for n in g.nodes()],
          node_color=range(len(g.nodes())),
          #edge_color=colorMap,
          cmap=plt.cm.Blues,
          # with_labels = True,
          )
  # nx.draw_networkx_labels(g, layout, labelsMap, font_size=8, font_color='r')
  
  # ax = plt.gca()
  fig = plt.gcf()
  # implot = ax.imshow(im)


  
  def onclick(event):
      if event.xdata != None and event.ydata != None:
          # print(event.xdata, event.ydata)
          closest = min(layout.keys(), key=lambda x: dist(layout[x][0], layout[x][1], event.xdata, event.ydata))
          print closest
          labelsMap = defaultdict(int)
          labelsMap[closest] = url_mapping[closest]
          if event.button==1:
            nx.draw_networkx_labels(g, layout, labelsMap, font_size=8, font_color='r')
          if event.button==3:
            webbrowser.open(url_mapping[closest])
          
          #plt.cla()
          plt.draw()


          
  cid = fig.canvas.mpl_connect('button_press_event', onclick)
  
  plt.show()

def dist(a, b, x, y):
  return math.sqrt((a - x) * (a - x) + (b - y) * (b - y))

def init():
  history_list, url_mapping = extract_history_records()
  
  print sys.argv
  if len(sys.argv) != 2:
    print 'needs layout argument'
    sys.exit(1)
    
  layout = sys.argv[1]
  
  if layout == '--circular':
    layout = nx.circular_layout
  elif layout == '--shell':
    layout = nx.shell_layout
    print 'shell'
  elif layout == '--graphviz':
    layout = nx.graphviz_layout
  elif layout == '--fruchterman':
    layout = nx.fruchterman_reingold_layout
  elif layout == '--random':
    layout = nx.random_layout
  elif layout == '--spring':
    layout = nx.spring_layout
  elif layout == '--spectral':
    layout = nx.spectral_layout
  else:
    print 'must specify valid layout'
    sys.exit(1)
    
  #layoutMethod = nx.circular_layout
  visualize(history_list, url_mapping, layout)
  
init()
