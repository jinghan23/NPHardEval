'''
To construct the dataset of graph vertex coloring, the following steps can be followed:

Use GrinPy2 and other necessary packages to generate and manipulate the graphs.
Create an Erdos-Rényi graph with varying node counts.
Check if the generated graph is planar.
Check if the graph is isomorphic to a previously generated one.
If both conditions are satisfied, calculate the chromatic number of the graph.
Convert the graph to the DIMACS format, appending a comment with the chromatic number.
Repeat the process until 100 instances with an average of 24 edges each are generated.
'''

import os
from grinpy import graph_clique_number
import grinpy as gp #gp==19.7a0
import networkx as nx # nx==3.1
from itertools import combinations

DATA_PATH = '../Data/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

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
def generate_instances(avg_edges_list, node_counts_list, num_instances_per_level, num_complexity_levels):
    # calculate number of instances per level
    print("There are {} instances per level".format(num_instances_per_level))

    # For each complexity level, generate instances
    for i in range(num_complexity_levels):
        print("Generating instances for level {}".format(i))

        # initiate graphs and dimacs_outputs
        graphs = []
        dimacs_outputs = []

        # retrieve average edges and range of node counts from avg_edges_list and node_counts_list
        avg_edges = avg_edges_list[i]
        node_counts = node_counts_list[i]

        # For each level, generate instances
        # There can be more than one instance per level
        j = 0
        while(j < num_instances_per_level):
            j += 1

            # Heuristic approach: vary n to approach the desired average edges for Erdos-Rényi graph
            for n in node_counts:
                potential_g = generate_graph(n, previous_graphs=graphs)
                if abs(potential_g.number_of_edges() - avg_edges) < n/2:  # Accept graph if within range
                    graphs.append(potential_g)
                    dimacs_outputs.append(graph_to_dimacs(potential_g))
                    break
                else:
                    j -= 1

        # Now, dimacs_outputs contains the DIMACS representations of the generated graphs
        # Save them to files in the data folder one level above

        with open(DATA_PATH+'synthesized_data_GCP_'+str(i)+'.txt', 'w') as file:
            for output in dimacs_outputs[:num_instances_per_level]:
                file.write(output + '\n\n')  # Separate each graph by two newline characters

num_instances_per_level = 20
num_complexity_levels = 5
avg_edges_list=[6, 10, 14, 18, 22]
node_counts_list = [range(6,8),range(8,10),range(10,12),range(12,14),range(14,16)]
generate_instances(avg_edges_list, node_counts_list, num_instances_per_level, num_complexity_levels)

# ### OG code
# graphs = []
# dimacs_outputs = []

# # Set desired average edges and range of node counts
# avg_edges = 24
# node_counts = range(10, 18)  # 10 to 17 inclusive


# for _ in range(100):
#     # Heuristic approach: vary n to approach the desired average edges for Erdos-Rényi graph
#     for n in node_counts:
#         potential_g = generate_graph(n, previous_graphs=graphs)
#         if abs(potential_g.number_of_edges() - avg_edges) < n/2:  # Accept graph if within range
#             graphs.append(potential_g)
#             dimacs_outputs.append(graph_to_dimacs(potential_g))
#             break

# # Now, dimacs_outputs contains the DIMACS representations of the generated graphs
# # Save them to files in the data folder one level above

# with open(DATA_PATH+'synthesized_data_GCP_1.txt', 'w') as file:
#     for output in dimacs_outputs:
#         file.write(output + '\n\n')  # Separate each graph by two newline characters
