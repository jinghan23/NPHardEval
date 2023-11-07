'''
The generate_msp_instance function generates a single problem instance with a specified number of meetings, participants, and time slots, as well as a complexity level.
The generate_msp_instances function generates multiple instances, using a list of complexity parameters to vary the complexity of each generated instance.
The save_instances_to_json function saves all generated instances to a JSON file for later use.
'''

import random
import json

DATA_PATH = '../Data/MSP/'

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
# num_participants = 1.5 num_meetings （round down）
# num_time_slots = 2 num_participants
# for 10 levels
complexity_params = [
    (4, 6, 8),  # Level 1
    (5, 7, 10),  # Level 2
    (6, 9, 12),  # Level 3
    (7, 10, 14),  # Level 4
    (8, 12, 16),  # Level 5
    (9, 13, 18),  # Level 6
    (10, 15, 20),  # Level 7
    (11, 16, 22),  # Level 8
    (12, 18, 24),  # Level 9
    (13, 19, 26)  # Level 10
]

# Example usage:
num_instances = 10  # Number of instances to generate per complexity level
instances = generate_msp_instances(num_instances, complexity_params)
save_instances_to_json(instances, DATA_PATH+'msp_instances.json')
