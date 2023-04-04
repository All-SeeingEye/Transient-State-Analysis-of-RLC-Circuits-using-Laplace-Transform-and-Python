import networkx as nx
import matplotlib.pyplot as plt
from parsing_circuit import *
import sys
#parsing
if len(sys.argv) != 3:
    print("Usage: python circuit_solve.py <input> <input>")
    sys.exit(1)

data = parse_circuit(sys.argv[1])
netlist_un,_,_,_,_ = process_net(data)
print(netlist_un)
netlist = parser_for_draw(netlist_un)
    

G = nx.Graph()

nodes = set([row[1] for row in netlist] + [row[2] for row in netlist] + ['0'])
for node in nodes:
    G.add_node(node)


for row in netlist:
    node1 = row[1]
    node2 = row[2]
    G.add_edge(node1, node2, label=row[0])


pos = nx.planar_layout(G)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)


edge_labels = {(edge[0], edge[1]): data['label'] for edge, data in G.edges.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.xlabel('Component')
plt.ylabel('Node')
plt.show()
