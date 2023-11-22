import os
import random
import json

DATA_PATH = '../Data/SPP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

# Function to generate a random graph instance
def generate_spp_instance(num_nodes, num_edges, max_weight, complexity_level):
    instance = {
        'nodes': list(range(num_nodes)),
        'edges': [],
        'complexity_level': complexity_level
    }

    # Ensure that the number of edges does not exceed the maximum possible for a simple graph
    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    num_edges = min(num_edges, max_possible_edges)

    # Create a set to track which edges have been added (to avoid duplicates)
    added_edges = set()

    while len(instance['edges']) < num_edges:
        # Randomly choose two different nodes
        u, v = random.sample(instance['nodes'], 2)

        # Ensure no duplicate edges and self-loops
        if u != v and (u, v) not in added_edges and (v, u) not in added_edges:
            weight = random.randint(1, max_weight)
            instance['edges'].append({'from': u, 'to': v, 'weight': weight})
            added_edges.add((u, v))

    return instance

# Generate a list of problem instances with varying complexity levels
def generate_spp_instances(num_instances, complexity_params):
    instances = []
    for complexity_param in complexity_params:
        for _ in range(num_instances):
            instance = generate_spp_instance(*complexity_param, complexity_level=complexity_param[0]-1)
            instances.append(instance)
    return instances

# Save the instances to a JSON file
def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (num_nodes, num_edges, max_weight)
complexity_params = [
    (4, 5, 6),  # Level 1
    (5, 6, 7),  # Level 2
    (6, 7, 8),  # Level 3
    (7, 8, 9),  # Level 4
    (8, 9, 10),  # Level 5
    (9, 10, 11),  # Level 6
    (10, 11, 12),  # Level 7
    (11, 12, 13)  # Level 8
    (12, 13, 14)  # Level 9
    (13, 14, 15)  # Level 10
]

# Example usage:
num_instances = 10  # Number of instances to generate per complexity level
instances = generate_spp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'spp_instances.json')