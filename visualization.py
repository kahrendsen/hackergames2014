import networkx as nx
import matplotlib.pyplot as plt
g=nx.DiGraph()
g.add_node("google.com")
g.add_node("facebook.com")
g.add_node("reddit.com")
g.add_node("twitter.com")
g.add_node("youtube.com")
g.add_node("linkedin.com")
g.add_node("yahoo.com")

g.add_edges_from([("google.com","facebook.com"),
	("facebook.com","twitter.com"),("google.com","reddit.com"),
	("reddit.com","youtube.com"),("reddit.com","linkedin.com"),
	("linkedin.com","yahoo.com"),("yahoo.com","reddit.com")])
nx.draw_circular(g, with_labels=True)
plt.show()
