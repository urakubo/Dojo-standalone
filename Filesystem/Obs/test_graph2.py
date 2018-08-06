#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import networkx as nx


G = nx.Graph() # unidirectional graph

anum = 6

G.add_edge(1,1+anum)
G.add_edge(2,2+anum)
G.add_edge(3,3+anum)
G.add_edge(4,4+anum)
# G[4][5+anum].update()
G.add_edges_from([(1,2+anum),(3,3+anum),(4,3+anum)])
## convenient way to add weighted edges

# G.add_nodes_from([3,15,16,17], weight=0.4)

print G.nodes()
print G.edges()

# c = nx.connected_components(G)

print 'True if the graph is connected, False otherwise.: ', nx.is_connected(G)
print 'Number of connected components: ', nx.number_connected_components(G)

sub_graphs = nx.connected_component_subgraphs(G)
#for i, sg in enumerate(sub_graphs):
#    print "subgraph {} has {} nodes".format(i, sg.number_of_nodes())
#    print "\tNodes:", sg.nodes(data=True)
#    print "\tEdges:", sg.edges()

for i, sg in enumerate(sub_graphs):
    print "subgraph {} has {} nodes".format(i, sg.number_of_nodes())
    print "\tNodes:", sg.nodes(data=False) # default=False

for i, sg in enumerate(sub_graphs):
    ggroup = sg.number_of_nodes()



# print 'Return the set of nodes in the component of graph: '
# for i in range(nx.number_connected_components(G)) :
#     print 'No', i, ', Con: ', nx.node_connected_component(G, i)


import matplotlib.pyplot as plt
nx.draw_networkx(G)
plt.show()

#連結成分分解
#components = nx.component.connected_components(G)
#print components

