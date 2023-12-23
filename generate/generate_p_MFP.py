import os
import random
import json

DATA_PATH = '../Data/MFP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

# Function to generate a random flow network
def generate_mfp_instance(num_nodes, num_edges, capacity_range, complexity_level):
    instance = {
        'nodes': num_nodes,
        'edges': [],
        'source': 0,
        'sink': num_nodes - 1,
        'complexity_level': complexity_level
    }

    for _ in range(num_edges):
        from_node = random.randint(0, num_nodes - 2)  # Exclude the sink node
        to_node = random.randint(from_node + 1, num_nodes - 1)  # Ensure flow direction
        capacity = random.randint(*capacity_range)
        edge = {'from': from_node, 'to': to_node, 'capacity': capacity}
        instance['edges'].append(edge)

    return instance

# Generate a list of problem instances with varying complexity levels
def generate_mfp_instances(num_instances, complexity_params):
    instances = []
    for complexity_param in complexity_params:
        for _ in range(num_instances):
            instance = generate_mfp_instance(*complexity_param, complexity_level=complexity_param[0] - 1)
            instances.append(instance)
    return instances

# Save the instances to a JSON file
def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (num_nodes, num_edges, capacity_range)
complexity_params = [
    (4, 6, (1, 4)),  # Level 1
    (5, 7, (1, 5)),  # Level 2
    (6, 8, (1, 6)),  # Level 3
    (7, 9, (1, 7)),  # Level 4
    (8, 10, (1, 8)),  # Level 5
    (9, 11, (1, 9)),  # Level 6
    (10, 12, (1, 10)),  # Level 7
    (11, 13, (1, 11)),  # Level 8
    (12, 14, (1, 12)),  # Level 9
    (13, 15, (1, 13)),  # Level 10
]


if __name__ == '__main__':
    # Example usage:
    num_instances = 10  # Number of instances to generate per complexity level
    instances = generate_mfp_instances(num_instances, complexity_params)
    save_instances_to_json(instances, DATA_PATH + 'mfp_instances.json')
