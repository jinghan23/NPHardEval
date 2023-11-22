import os
import grinpy as gp
import networkx as nx
from itertools import combinations

DATA_PATH = '../Data/GCP_Decision/'
os.makedirs(DATA_PATH, exist_ok=True)

def is_isomorphic_to_any(graph, graph_list):
    for g in graph_list:
        if nx.is_isomorphic(graph, g):
            return True
    return False

def generate_graph(n, p=0.4, previous_graphs=[]):
    while True:
        g = nx.erdos_renyi_graph(n, p)
        if nx.check_planarity(g)[0] and not is_isomorphic_to_any(g, previous_graphs):
            return g

def graph_to_dimacs(g, k_colors):
    # can_be_colored = gp.is_k_colorable(g, k_colors)
    # colorable_text = "YES" if can_be_colored else "NO"
    lines = []
    lines.append(f"c This graph can be colored with {k_colors} colors")
    lines.append("p edge {} {}".format(g.number_of_nodes(), g.number_of_edges()))
    for u, v in g.edges():
        lines.append("e {} {}".format(u + 1, v + 1))
    return "\n".join(lines)

def generate_instances(avg_edges_list, node_counts_list, num_instances_per_level, num_complexity_levels, k_colors):
    print("There are {} instances per level".format(num_instances_per_level))

    for i in range(num_complexity_levels):
        print("Generating instances for level {}".format(i))
        graphs = []
        dimacs_outputs = []

        avg_edges = avg_edges_list[i]
        node_counts = node_counts_list[i]

        j = 0
        while(j < num_instances_per_level):
            j += 1

            for n in node_counts:
                potential_g = generate_graph(n, previous_graphs=graphs)
                if abs(potential_g.number_of_edges() - avg_edges) < n/2:
                    graphs.append(potential_g)
                    dimacs_outputs.append(graph_to_dimacs(potential_g, k_colors))
                    break
                else:
                    j -= 1

        with open(DATA_PATH+'decision_data_GCP_'+str(i)+'.txt', 'w') as file:
            for output in dimacs_outputs[:num_instances_per_level]:
                file.write(output + '\n\n')

num_instances_per_level = 10
num_complexity_levels = 10
avg_edges_list = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
node_counts_list = [range(6,7), range(7,8), range(8,9), range(9,10), range(10,11), range(11,12), range(12,13), range(13,14), range(14,15), range(15,16)]
k_colors = 3  # Specify the target number of colors here
generate_instances(avg_edges_list, node_counts_list, num_instances_per_level, num_complexity_levels, k_colors)
