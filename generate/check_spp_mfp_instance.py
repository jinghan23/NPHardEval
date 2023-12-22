import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from check.check_p_SPP import ssp_optimal_solution
from check.check_p_MFP import mfp_check
from run_close_zero.utils import parse_xml_to_dict

import random
import pandas as pd
import numpy as np
import json
import argparse

from deepdiff import DeepDiff

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

def load_spp_data():
    data_path = '../Data/SPP/'
    with open(data_path + "spp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data

def load_mfp_data():
    data_path = '../Data/MFP/'
    with open(data_path + "mfp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data

def runSPP_check(q):
    A, B = ssp_optimal_solution(q, q['nodes'][0], q['nodes'][-1]) 
    return A == None

def runMFP_check(q):
    A, B = mfp_check(q, {})
    return A

def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)


if __name__ == '__main__':

    spp_complexity_params = [
        (4, 5, 6),  # Level 1
        (5, 6, 7),  # Level 2
        (6, 7, 8),  # Level 3
        (7, 8, 9),  # Level 4
        (8, 9, 10),  # Level 5
        (9, 10, 11),  # Level 6
        (10, 11, 12),  # Level 7
        (11, 12, 13),  # Level 8
        (12, 13, 14),  # Level 9
        (13, 14, 15)  # Level 10
    ]

    mfp_complexity_params = [
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

    num_instances = 10  # Number of instances to generate per complexity level

    spp_instances = generate_spp_instances(num_instances, spp_complexity_params)
    mfp_instances = generate_mfp_instances(num_instances, mfp_complexity_params)

    convex = [
        ('spp', load_spp_data, runSPP_check, spp_instances),
        ('mfp', load_mfp_data, runMFP_check, mfp_instances)
    ]

    for name, load_func, check_func, new_instances in convex:
        sppData = load_func()
        old_instances = [sppData[i:i+10] for i in range(0, len(sppData), 10)]
        new_instances = [new_instances[i:i+10] for i in range(0, len(new_instances), 10)]
        sppResults = []

        spp_new_instances = []

        for old_data, new_data in zip(old_instances, new_instances):
            a = []
            cnt = 0
            replace_pos = []
            for i, q in enumerate(old_data):
                if check_func(q):
                    cnt += 1
                    replace_pos.append(i)
                    sppResults.append(1)
                else:
                    sppResults.append(0)
            
            if cnt > 0:
                satisfied_instance = [q for q in new_data if not check_func(q)]
                satisfied_instance = [q for q in satisfied_instance if all(DeepDiff(q, q2) for q2 in old_data)]
                satisfied_instance = satisfied_instance[:cnt]
                for pos, instance in zip(replace_pos, satisfied_instance):
                    instance['replace_pos'] = pos
                # print(cnt, len(satisfied_instance))
                # print(satisfied_instance[-1]['complexity_level'])
                spp_new_instances += satisfied_instance

        sppResults = np.array(sppResults).reshape(-1, 10).mean(axis=1)
        print(f"{name}:", sppResults, sppResults.mean())
        save_instances_to_json(spp_new_instances, f'{name}_instances.json')