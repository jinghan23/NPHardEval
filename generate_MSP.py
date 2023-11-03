'''
The generate_msp_instance function generates a single problem instance with a specified number of meetings, participants, and time slots, as well as a complexity level.
The generate_msp_instances function generates multiple instances, using a list of complexity parameters to vary the complexity of each generated instance.
The save_instances_to_json function saves all generated instances to a JSON file for later use.
'''

import random
import json

DATA_PATH = '../Data/'

# Function to generate random meetings, participants, and time slots
def generate_msp_instance(num_meetings, num_participants, num_time_slots, complexity_level):
    # Initialize the problem instance dictionary
    instance = {
        'meetings': [],
        'participants': {},
        'time_slots': num_time_slots,
        'complexity_level': complexity_level
    }
    
    # Create meetings with random durations
    for m_id in range(num_meetings):
        meeting = {
            'id': m_id,
            'duration': random.randint(1, 3)  # Duration between 1 to 3 time slots
        }
        instance['meetings'].append(meeting)
    
    # Assign participants to meetings
    for p_id in range(num_participants):
        instance['participants'][p_id] = {
            'available_slots': sorted(random.sample(range(num_time_slots), random.randint(1, num_time_slots))),
            'meetings': random.sample(range(num_meetings), random.randint(1, num_meetings))
        }

    return instance

# Generate a list of problem instances with varying complexity levels
def generate_msp_instances(num_instances, complexity_params):
    instances = []
    for i in range(num_instances):
        # Complexity parameters: (num_meetings, num_participants, num_time_slots)
        params = complexity_params[i % len(complexity_params)]
        instance = generate_msp_instance(*params, complexity_level=i % len(complexity_params) + 1)
        instances.append(instance)
    return instances

# Save the instances to a JSON file
def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (num_meetings, num_participants, num_time_slots)
complexity_params = [
    (5, 10, 10),  # Level 1: Simple
    (7, 15, 15),  # Level 2: Medium 1
    (10, 20, 20), # Level 2: Medium 2
    (15, 30, 30), # Level 3: Hard 1
    (20, 40, 40), # Level 3: Hard 2
]

# Example usage:
num_instances = 15  # Total number of instances to generate
instances = generate_msp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'msp_instances.json')
