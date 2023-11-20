import sys
import os
sibling_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generate'))
print(sibling_directory_path)
sys.path.append(sibling_directory_path)

from generate_GCP_D import *

def read_graph(file_path):
    return nx.read_adjlist(file_path)

def is_safe(graph, node, coloring, color):
    for neighbor in graph.neighbors(node):
        if coloring.get(neighbor) == color:
            return False
    return True

def graph_coloring_util(graph, m, coloring, node):
    if node == len(graph):
        return True

    for color in range(1, m + 1):
        if is_safe(graph, node, coloring, color):
            coloring[node] = color
            if graph_coloring_util(graph, m, coloring, node + 1):
                return True
            del coloring[node]  # Remove the assignment and try next color
    return False

def graph_coloring(graph, m):
    coloring = {}
    if graph_coloring_util(graph, m, coloring, 0):
        return coloring
    return None

def check_graph_coloring(file_path, num_colors):
    graph = read_graph(file_path)
    solution = graph_coloring(graph, num_colors)
    return solution is not None, solution

if __name__ == "__main__":
    graph_file = "../Data/GCP-D/graph_level_1_q_1.adjlist"
    num_colors = 3  # Example number of colors
    valid, solution = check_graph_coloring(graph_file, num_colors)
    if valid:
        print("A valid coloring exists:", solution)
    else:
        print("No valid coloring found.")

