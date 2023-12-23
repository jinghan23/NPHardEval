'''
The generate_msp_instance function generates a single problem instance with a specified number of meetings, participants, and time slots, as well as a complexity level.
The generate_msp_instances function generates multiple instances, using a list of complexity parameters to vary the complexity of each generated instance.
The save_instances_to_json function saves all generated instances to a JSON file for later use.
'''

import os
import random
import json

DATA_PATH = '../Data/MSP/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

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
            'duration': 1
            # 'duration': random.randint(1, 3)  # Duration between 1 to 3 time slots
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
    for complexity_param in complexity_params:
        for i in range(num_instances):
            instance = generate_msp_instance(*complexity_param, complexity_level=complexity_param[0]-1)
            instances.append(instance)
    # for i in range(num_instances):
    #     # Complexity parameters: (num_meetings, num_participants, num_time_slots)
    #     params = complexity_params[i % len(complexity_params)]
    #     instance = generate_msp_instance(*params, complexity_level=i % len(complexity_params) + 1)
    #     instances.append(instance)
    return instances

# Save the instances to a JSON file
def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)

# Define complexity levels based on a tuple of (num_meetings, num_participants, num_time_slots)
# num_participants = num_meetings + 1
# num_time_slots = num_meetings + 2
# for 10 levels
complexity_params = [
    (2, 3, 4),  # Level 1
    (3, 4, 5),  # Level 2
    (4, 5, 6),  # Level 3
    (5, 6, 7),  # Level 4
    (6, 7, 8),  # Level 5
    (7, 8, 9),  # Level 6
    (8, 9, 10),  # Level 7
    (9, 10, 11),  # Level 8
    (10, 11, 12),  # Level 9
    (11, 12, 13)  # Level 10
]

if __name__ == '__main__':
    # Example usage:
    num_instances = 10  # Number of instances to generate per complexity level
    instances = generate_msp_instances(num_instances, complexity_params)
    save_instances_to_json(instances, DATA_PATH+'msp_instances.json')
