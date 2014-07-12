import sqlite3

from igraph import *
import readhistory

placesPath = '../places.sqlite'

def extract_history_records():
  conn = sqlite3.connect(readhistory.get_places_path())
  c = conn.cursor()

  c.execute('select from_visit, place_id from moz_historyvisits')
  history = c.fetchall()

  c.execute('select id, url from moz_places')
  places = c.fetchall()
  
  id2url = dict(places)  
  id2url[0] = 'first_search'
  
  id2url = defaultdict(int, id2url)  # get rid of the key errors in id2url, but maybe problematic
  conn.close()
  
  return history, id2url

def main():
  history, id2url = extract_history_records()
  
  g = Graph()
  
  visited = set([a for tf in history for a in tf])
  print visited
  
  for url in id2url.values():
    g.add_vertex(url)
  
  for entry in history:
    fromUrl = id2url[entry[0]]
    toUrl = id2url[entry[1]]
    g.add_edge(fromUrl, toUrl)
    
  lay = g.layout_reingold_tilford_circular()
  plot(g, layout=lay,
       vertex_size=[min(40, g.degree(a, type='out')) for a in g.vs])
  
    
if __name__ == '__main__':
  main()
