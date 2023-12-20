import json
from collections import defaultdict
import networkx as nx

# Add the parent directory to the path
import sys
import pathlib
path = pathlib.Path(__file__).parent.parent.absolute().as_posix()
sys.path.append(path)
from check.check_p_MFP import mfp_check


def bfs_level_graph(graph, source, target):
    """Constructs level graph using BFS."""
    level = {v: -1 for v in graph}
    level[source] = 0
    queue = [source]

    while queue:
        u = queue.pop(0)
        for v in graph.neighbors(u):
            if level[v] < 0 and graph[u][v]['capacity'] - graph[u][v]['flow'] > 0:
                level[v] = level[u] + 1
                queue.append(v)
    return level


def dfs_find_blocking_flow(graph, u, flow, target, level):
    """Finds a blocking flow in the level graph using DFS."""
    if u == target:
        return flow, str(u)
    for v in graph[u]:
        if level[v] == level[u] + 1 and graph[u][v]['capacity'] - graph[u][v]['flow'] > 0:
            min_flow = min(flow, graph[u][v]['capacity'] - graph[u][v]['flow'] + graph[v][u]['flow'])
            flow_found, path = dfs_find_blocking_flow(graph, v, min_flow, target, level)
            if flow_found > 0:
                net_flow = graph[u][v]['flow'] + flow_found - graph[v][u]['flow']
                if net_flow > 0:
                    graph[u][v]['flow'] = net_flow
                    graph[v][u]['flow'] = 0
                else:
                    graph[u][v]['flow'] = 0
                    graph[v][u]['flow'] = -net_flow
                return flow_found, str(u) + "->" + path
    return 0, ""


def print_graph_capacity(graph, f):
    """Prints the capacity of each edge in the graph."""
    print("The edge capacities are: ", file=f)
    for i, (u, v) in enumerate(graph.edges()):
        net_capacity = graph[u][v]['capacity'] - graph[u][v]['flow'] + graph[v][u]['flow']
        print(f'{i}. the capacity of flow from {u} to {v} is {net_capacity} and the current flow is {graph[u][v]["flow"]}.', file=f)


def answer_generate_MFP_helper(num_nodes, edge_capacities, source, target, f):
    """Implements the algorithm for MFP."""
    # Construct the graph
    graph = nx.DiGraph()
    for i in range(num_nodes):
        graph.add_node(i)
    for edge, capacity in edge_capacities.items():
        u, v = edge.split('->')
        u, v = int(u), int(v)
        graph.add_edge(u, v, capacity=capacity, flow=0)
        graph.add_edge(v, u, capacity=capacity, flow=0)
    
    max_flow = 0
    while True:
        print_graph_capacity(graph, f)
        print("Considering edges with the capacity smaller than the current flow, one can navigate the graph with Breadth First Search to find the level graph:", file=f)
        levels = bfs_level_graph(graph, source, target)
        for i, (node, level) in enumerate(levels.items()):
            print(f'{i}. the level of node {node} is {level}.', file=f)
        if levels[target] < 0:
            print(f"As the sink node {target} with level {levels[target]} is not reachable from the source node {source}, the algorithm terminates.", file=f)
            break  # no more augmenting paths
        while True:
            flow, path = dfs_find_blocking_flow(graph, source, float('inf'), target, levels)
            if flow == 0:
                break
            print("Find a blocking flow: ", path, file=f)
            print("The blocking flow is: ", flow, file=f)
            max_flow += flow
        
    print("The max flow is: ", max_flow, file=f)
    flow_assignment = {}
    for u, v in graph.edges():
        if graph[u][v]['flow'] > 0:
            flow_assignment[f'{u}->{v}'] = graph[u][v]['flow']
    answer = {'MaxFlow': max_flow, 'Flows': flow_assignment}
    print("</reasoning>", file=f)
    print(f"<final_answer>{answer}</final_answer>", file=f)
    return answer


def answer_generate_MFP(instance, f):
    # Get the start and end nodes
    # Curently, the start and end nodes are the first and last nodes in the instance
    num_nodes = instance['nodes']
    start_node = instance['source']
    end_node = instance['sink']

    print("<root>", file=f)
    print("<reasoning>", file=f)
    # Initialize edge flows
    edges = instance['edges']
    edge_name_func = lambda from_node, to_node: f'{from_node}->{to_node}' if from_node < to_node else f'{to_node}->{from_node}'
    edge_capacities = defaultdict(int)
    for edge in edges:
        edge_name = edge_name_func(edge['from'], edge['to'])
        edge_capacities[edge_name] += int(edge['capacity'])
    
    print("Aggregated edge capacities: ", file=f)
    for i, (edge_name, capacity) in enumerate(edge_capacities.items()):
        node1, node2 = edge_name.split('->')
        print(f'{i}. the capacity of edge between {node1} and {node2} is {capacity}.', file=f)
    answer = answer_generate_MFP_helper(num_nodes, edge_capacities, start_node, end_node, f)
    print("</root>", file=f)
    return answer


def check_correctness(instance, f):
    answer = answer_generate_MFP(instance, f)
    return mfp_check(instance, answer)


# Example usage 1:
# Define an example MFP instance
with open("answer.txt", 'w') as f:
    mfp_instance =   {
        "nodes": 4,
        "edges": [
            {"from": 0, "to": 3, "capacity": 3},
            {"from": 0, "to": 3, "capacity": 4},
            {"from": 0, "to": 3, "capacity": 2},
            {"from": 2, "to": 3, "capacity": 3},
            {"from": 0, "to": 2, "capacity": 4},
            {"from": 1, "to": 2, "capacity": 3}
        ],
        "source": 0,
        "sink": 3,
        "complexity_level": 3
    }

    # Define a solution for the MFP instance
    mfp_solution = {"MaxFlow": 12, "Flows": {"0->3": 9, "0->2": 3, "2->3": 3}}

    # Validate the solution
    max_flow = answer_generate_MFP(mfp_instance, f)['MaxFlow']
    print("Correctness:", max_flow == mfp_solution['MaxFlow'])


# # Example usage 2:
# # DATA_PATH = '../Data/MFP/'
# DATA_PATH = './'

# def load_data():
#     data_path = DATA_PATH
#     with open(data_path + "mfp_instances.json", 'r') as f:
#         all_data = json.load(f)
#     return all_data

# cnt = 0
# data = load_data()
# for x in data:
#     if not check_correctness(x, f=sys.stdout):
#         cnt += 1
# print("Inconsistent instances:", cnt)