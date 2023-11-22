import os
import random
import json

DATA_PATH = '../Data/BSP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

def generate_bsp_instance(array_length, number_range):
    # Initialize the problem instance dictionary
    instance = {
        'array': sorted([random.randint(*number_range) for _ in range(array_length)]),
        'target': random.randint(*number_range)
    }

    # Ensure the target is in the array for a guaranteed solution
    if instance['target'] not in instance['array']:
        instance['array'][random.randint(0, array_length - 1)] = instance['target']

    return instance

def generate_bsp_instances(num_instances, complexity_params):
    instances = []
    for array_length, number_range in complexity_params:
        for _ in range(num_instances):
            instance = generate_bsp_instance(array_length, number_range)
            instances.append(instance)
    return instances

def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (array_length, number_range)
complexity_params = [
    (3, (1, 15)),  # Level 1
    (4, (1, 20)),  # Level 2
    (5, (1, 25)),  # Level 3
    (6, (1, 30)),  # Level 4
    (7, (1, 35)),  # Level 5
    (8, (1, 40)),  # Level 6
    (9, (1, 45)),  # Level 7
    (10, (1, 50)),  # Level 8
    (11, (1, 55)),  # Level 9
    (12, (1, 60)),  # Level 10
]

# Example usage:
num_instances = 10  # Number of instances to generate per complexity level
instances = generate_bsp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'bsp_instances.json')
