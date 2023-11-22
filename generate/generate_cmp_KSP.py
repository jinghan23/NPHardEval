import os
import random
import json

DATA_PATH = '../Data/KSP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

def generate_ksp_instance(num_items, weight_range, value_range, knapsack_capacity):
    # Initialize the problem instance dictionary
    instance = {
        'items': [],
        'knapsack_capacity': knapsack_capacity
    }

    # Create items with random weights and values
    for item_id in range(num_items):
        item = {
            'id': item_id,
            'weight': random.randint(*weight_range),
            'value': random.randint(*value_range)
        }
        instance['items'].append(item)

    return instance

def generate_ksp_instances(num_instances, complexity_params):
    instances = []
    for complexity_param in complexity_params:
        for i in range(num_instances):
            instance = generate_ksp_instance(*complexity_param)
            instances.append(instance)
    return instances

def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (num_items, weight_range, value_range, knapsack_capacity)
complexity_params = [
    (4, (1, 4), (1, 4), 20),  # Level 1
    (5, (1, 5), (1, 5), 25),  # Level 2
    (6, (1, 6), (1, 6), 30),  # Level 3
    (7, (1, 7), (1, 7), 35),  # Level 4
    (8, (1, 8), (1, 8), 40),  # Level 5
    (9, (1, 9), (1, 9), 45),  # Level 6
    (10, (1, 10), (1, 10), 50),  # Level 7
    (11, (1, 11), (1, 11), 55),  # Level 8
    (12, (1, 12), (1, 12), 60),  # Level 9
    (13, (1, 13), (1, 13), 65),  # Level 10
]

# Example usage:
num_instances = 10  # Number of instances to generate per complexity level
instances = generate_ksp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'ksp_instances.json')
