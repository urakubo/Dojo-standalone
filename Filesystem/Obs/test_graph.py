#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import networkx as nx

#二項分布(p=0.1)に従ってリンクの張られるランダムネットワーク
G = nx.binomial_graph(10,0.1)
G.add_nodes_from([11,12,13,14])
G.add_edge(1,2)
G.add_edge(3,4)
G.add_edge(10,11)
G.add_edge(12,13)
G.add_edge(10,14)

G.add_edges_from([(0,1),(1,2),(15,2)])
## convenient way to add weighted edges

G.add_nodes_from([3,15,16,17], weight=0.4)


print G.nodes()
print G.edges()

# c = nx.connected_components(G)

print 'True if the graph is connected, False otherwise.: ', nx.is_connected(G)
print 'Number of connected components: ', nx.number_connected_components(G)

# make an undirected copy of the digraph
UG = G.to_undirected()
# extract subgraphs
sub_graphs = nx.connected_component_subgraphs(UG)
#for i, sg in enumerate(sub_graphs):
#    print "subgraph {} has {} nodes".format(i, sg.number_of_nodes())
#    print "\tNodes:", sg.nodes(data=True)
#    print "\tEdges:", sg.edges()

for i, sg in enumerate(sub_graphs):
    print "subgraph {} has {} nodes".format(i, sg.number_of_nodes())
    print "\tNodes:", sg.nodes(data=False) # default=False

# print 'Return the set of nodes in the component of graph: '
# for i in range(nx.number_connected_components(G)) :
#     print 'No', i, ', Con: ', nx.node_connected_component(G, i)


import matplotlib.pyplot as plt
nx.draw_networkx(G)
plt.show()

#連結成分分解
#components = nx.component.connected_components(G)
#print components

