'''
To construct the dataset of graph vertex coloring, the following steps can be followed:

Use GrinPy2 and other necessary packages to generate and manipulate the graphs.
Create an Erdos-Rényi graph with varying node counts from 10 to 17.
Check if the generated graph is planar.
Check if the graph is isomorphic to a previously generated one.
If both conditions are satisfied, calculate the chromatic number of the graph.
Convert the graph to the DIMACS format, appending a comment with the chromatic number.
Repeat the process until 100 instances with an average of 24 edges each are generated.
'''

import grinpy as gp
import networkx as nx
from itertools import combinations

# Check if a graph is isomorphic to any graph in a list of graphs
def is_isomorphic_to_any(graph, graph_list):
    for g in graph_list:
        if nx.is_isomorphic(graph, g):
            return True
    return False

# Generate a graph using the Erdos-Rényi method, ensuring it's planar and not isomorphic to previous graphs
def generate_graph(n, p=0.4, previous_graphs=[]):
    while True:
        g = nx.erdos_renyi_graph(n, p)
        if nx.check_planarity(g)[0] and not is_isomorphic_to_any(g, previous_graphs):
            return g

# Convert a graph to DIMACS format with a comment containing its chromatic number
def graph_to_dimacs(g):
    chromatic_num = gp.chromatic_number(g)
    lines = []
    lines.append("c This is a generated graph with chromatic number {}".format(chromatic_num))
    lines.append("p edge {} {}".format(g.number_of_nodes(), g.number_of_edges()))
    for u, v in g.edges():
        lines.append("e {} {}".format(u + 1, v + 1))  # DIMACS format uses 1-based indices
    return "\n".join(lines)

# Generate 100 instances
graphs = []
dimacs_outputs = []

# Set desired average edges and range of node counts
avg_edges = 24
node_counts = range(10, 18)  # 10 to 17 inclusive

for _ in range(100):
    # Heuristic approach: vary n to approach the desired average edges for Erdos-Rényi graph
    for n in node_counts:
        potential_g = generate_graph(n, previous_graphs=graphs)
        if abs(potential_g.number_of_edges() - avg_edges) < n/2:  # Accept graph if within range
            graphs.append(potential_g)
            dimacs_outputs.append(graph_to_dimacs(potential_g))
            break

# Now, dimacs_outputs contains the DIMACS representations of the generated graphs
# Save them to files in the data folder one level above
DATA_PATH = '../Data/'
with open(DATA_PATH+'synthesized_dimacs_graphs.txt', 'w') as file:
    for output in dimacs_outputs:
        file.write(output + '\n\n')  # Separate each graph by two newline characters
