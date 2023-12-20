import os
import random
import json
import string

DATA_PATH = '../Data/EDP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

def generate_edp_instance(length_a, length_b, char_range):
    # Generate two random strings of specified lengths and character ranges
    string_a = ''.join(random.choices(char_range, k=length_a))
    string_b = ''.join(random.choices(char_range, k=length_b))

    return {
        'string_a': string_a,
        'string_b': string_b
    }

def generate_edp_instances(num_instances, complexity_params):
    instances = []
    for length_a, length_b, char_range in complexity_params:
        for _ in range(num_instances):
            instance = generate_edp_instance(length_a, length_b, char_range)
            instances.append(instance)
    return instances

def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (length_a, length_b, char_range)
complexity_params = [
    (3, 3, string.ascii_lowercase[:6]),   # Level 1
    (4, 4, string.ascii_lowercase[:8]),   # Level 2
    (5, 5, string.ascii_lowercase[:10]),  # Level 3
    (6, 6, string.ascii_lowercase[:12]),  # Level 4
    (7, 7, string.ascii_lowercase[:14]),  # Level 5
    (8, 8, string.ascii_lowercase[:16]),  # Level 6
    (9, 9, string.ascii_lowercase[:18]),  # Level 7
    (10, 10, string.ascii_lowercase[:20]),  # Level 8
    (11, 11, string.ascii_lowercase[:22]),  # Level 9
    (12, 12, string.ascii_lowercase[:24]),  # Level 10
]

# Example usage:
num_instances = 10  # Number of instances to generate per complexity level
instances = generate_edp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'edp_instances.json')
