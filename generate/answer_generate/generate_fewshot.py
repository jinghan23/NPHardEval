import os
import random
import json
import argparse
from generate import *
from run import *
import time
from tqdm import tqdm 


import ast
def parse_xml_to_dict(xml_string):
    try:
        assert '<final_answer>' in xml_string
        assert '</final_answer>' in xml_string
        #assert '<reasoning>' in xml_string 
        #assert '</reasoning>' in xml_string
        final_answer_start = xml_string.index('<final_answer>') + len('<final_answer>') 
        final_answer_end = xml_string.index('</final_answer>')
        #reasoning_start = xml_string.index('<reasoning>') + len('<reasoning>')
        #reasoning_end = xml_string.index('</reasoning>')
        final_answer_element  = xml_string[final_answer_start:final_answer_end].rstrip().strip().rstrip()
        assert '{' in final_answer_element
        assert '}' in final_answer_element
        dic_start = final_answer_element.index('{')
        dic_end = final_answer_element.index('}')
        final_answer_element = final_answer_element[dic_start:dic_end+1].rstrip().strip().rstrip()
        reasoning_element = xml_string
        #reasoning_element = xml_string[reasoning_start:reasoning_end].rstrip().strip().rstrip()
        try:
            final_answer_element = ast.literal_eval(final_answer_element)
        except:
            final_answer_element = ''
    except:
        final_answer_element = ''
        reasoning_element = ''

    return final_answer_element, reasoning_element

def generate_instances_function(args):
    if args.type == 'BSP':
        return generate_bsp_instances
    elif args.type == 'EDP':
        return generate_edp_instances
    elif args.type == 'MFP':
        return generate_mfp_instances
    elif args.type == 'SPP':
        return generate_spp_instances
    elif args.type == 'TSP':
        return generate_tsp_instances
    elif args.type == 'GCP':
        return generate_gcp_instances
    elif args.type == 'MSP':
        return generate_msp_instances
    elif args.type == 'KSP':
        return generate_ksp_instances
    elif args.type == 'GCP_D':
        return generate_GCP_D_instances
    elif args.type == 'TSP_D':
        return generate_tsp_instances
    else:
        raise ValueError('Invalid problem type')

def run_gpt_function(args):
    if args.type == 'BSP':
        return runBSP
    elif args.type == 'EDP':
        return runEDP
    elif args.type == 'MFP':
        return runMFP
    elif args.type == 'SPP':
        return runSPP
    elif args.type == 'TSP':
        return runTSP
    elif args.type == 'GCP':
        return runGCP
    elif args.type == 'MSP':
        return runMSP
    elif args.type == 'KSP':
        return runKSP
    elif args.type == 'GCP_D':
        return runGCP_D
    elif args.type == 'TSP_D':
        return runTSP_D
    else:
        raise ValueError('Invalid problem type')


def generate_complexity_params(args):
    if args.type == 'BSP':
        return {"num_instances":20,
                "complexity_params":[
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
                    (13, (1, 65)),  # Level 1
                    (14, (1, 70)),  # Level 2
                    (15, (1, 75)),  # Level 3
                    (16, (1, 80)),  # Level 4
                    (17, (1, 85)),  # Level 5
                    (18, (1, 90)),  # Level 6
                    (19, (1, 95)),  # Level 7
                    (20, (1, 100)),  # Level 8
                    (21, (1, 105)),  # Level 9
                    (22, (1, 110)),  # Level 10
                ]
            }
    elif args.type == 'MFP':
        return {"num_instances":50,
                "complexity_params":[
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
                    (14, 16, (1, 14)),  # Level 1
                    (15, 17, (1, 15)),  # Level 2
                    (16, 18, (1, 16)),  # Level 3
                    (17, 19, (1, 17)),  # Level 4
                    (18, 20, (1, 18)),  # Level 5
                    (19, 21, (1, 19)),  # Level 6
                    (20, 22, (1, 20)),  # Level 7
                    (21, 23, (1, 21)),  # Level 8
                    (22, 24, (1, 22)),  # Level 9
                    (23, 25, (1, 23)),  # Level 10
                ]
            }
    elif args.type == 'SPP':
        return {"num_instances":20,
                "complexity_params":[
                    (4, 5, 6),  # Level 1
                    (5, 6, 7),  # Level 2
                    (6, 7, 8),  # Level 3
                    (7, 8, 9),  # Level 4
                    (8, 9, 10),  # Level 5
                    (9, 10, 11),  # Level 6
                    (10, 11, 12),  # Level 7
                    (11, 12, 13),  # Level 8
                    (12, 13, 14),  # Level 9
                    (13, 14, 15),  # Level 10
                    (14, 15, 16),  # Level 1
                    (15, 16, 17),  # Level 2
                    (16, 17, 18),  # Level 3
                    (17, 18, 19),  # Level 4
                    (18, 19, 20),  # Level 5
                    (19, 20, 21),  # Level 6
                    (20, 21, 22),  # Level 7
                    (21, 22, 23),  # Level 8
                    (22, 23, 24),  # Level 9
                    (23, 24, 25),  # Level 10
                ]
        }
    elif args.type == 'EDP':
        return {"num_instances":20,
                "complexity_params":[
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
                    (13, 13, string.ascii_lowercase[:26]),   # Level 11
                    (14, 14, string.ascii_lowercase[:28]),   # Level 12
                    (15, 15, string.ascii_lowercase[:30]),  # Level 13
                    (16, 16, string.ascii_lowercase[:32]),  # Level 14
                    (17, 17, string.ascii_lowercase[:34]),  # Level 15
                    (18, 18, string.ascii_lowercase[:36]),  # Level 16
                    (19, 19, string.ascii_lowercase[:38]),  # Level 17
                    (20, 20, string.ascii_lowercase[:40]),  # Level 18
                    (21, 21, string.ascii_lowercase[:42]),  # Level 19
                    (22, 22, string.ascii_lowercase[:44]),  # Level 20
                ]
        }
    elif args.type == 'TSP':
        # complexity level is the number of nodes
        return {"num_instances_per_level":20, "node_nums":[4, 5, 6, 7, 8, 9, 10, 11, 12, 13]}
    elif args.type == 'GCP':
        # complexity level is a pair lf (avg_edges, node_counts)
        return {
                "num_instances_per_level":20,
                "num_complexity_levels":10,
                "avg_edges_list":[6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
                "node_counts_list":[range(6,7),range(7,8),range(8,9),range(9,10),range(10,11),range(11,12),range(12,13),range(13,14),range(14,15),range(15,16)]
            }
    elif args.type == 'MSP':
        return {"num_instances":20,
                "complexity_params":[
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
        }
    elif args.type == 'KSP':
        return {"num_instances":20,
                "complexity_params":[
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
        }
    elif args.type == 'GCP_D':
        # complexity level is a pair lf (avg_edges, node_counts)
        return {
                "num_instances_per_level":2010,
                "num_complexity_levels":10,
                "avg_edges_list":[6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
                "node_counts_list":[range(6,7), range(7,8), range(8,9), range(9,10), range(10,11), range(11,12), range(12,13), range(13,14), range(14,15), range(15,16)],
                "k_colors":3
            }
    elif args.type == 'TSP_D':
        return {
            "num_instances_per_level":20,
            "node_nums":[4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            "threshold_factor":0.75
        }
    else:
        raise ValueError('Invalid problem type')


def check_correctness_function(args, result, instance):
    if args.type == 'BSP':
        correctness = bsp_check(instance, result)
        return correctness, result
    if args.type == 'EDP':
        correctness = edp_check(instance, result)
        return correctness, result
    elif args.type == 'MFP':
        correctness = mfp_check(instance, result)
        return correctness, result
    elif args.type == 'SPP':
        correctness = spp_check(instance, result)
        return correctness, result
    elif args.type == 'TSP':
        correctness = tspCheck(instance, result)
        return correctness, output
    elif args.type == 'GCP':
        correctness = gcpCheck(instance, result)
        return correctness, output
    elif args.type == 'MSP':
        correctness = mspCheck(instance, result)
        return correctness, output
    elif args.type == 'KSP':
        output, _ = parse_xml_to_dict(result)
        correctness = kspCheck(instance, output)
        return correctness, output
    elif args.type == 'GCP_D':
        number_of_colors = int(instance.split('\n')[0].split()[-2])
        output, _ = parse_xml_to_dict(result)
        correctness = gcp_decision_check(instance, output, number_of_colors)
        return correctness, output
    elif args.type == 'TSP_D':
        return None, None
    else:
        raise ValueError('Invalid problem type')

def generate_few_shot_instances(generate_datapoint_function, run_gpt, params, test_data,MODEL):
    fewshots = []
    num_complexity_levels = 20
    all_generated  =[]
    for i in tqdm(range(num_complexity_levels)):
        one_params = params.copy()
        one_params['complexity_params'] = [params['complexity_params'][i]]
        instances = generate_datapoint_function(**one_params)
        for instance in instances:
            if instance not in test_data:
                while True:
                    try:
                        output = run_gpt(MODEL,instance)
                        break
                    except:
                        time.sleep(1)
                result, _ = parse_xml_to_dict(output)
                correctness, _ = check_correctness_function(args, result, instance)
                if correctness[0] and '</final_answer>' in output and 'N/A' not in output and 'UNKNOWN' not in output:
                    print(result)
                    print('----------')
                    fewshots.append({'question':instance, 'output':output, 'complexity_level':i+1})
                else:
                    all_generated.append({'question':instance, 'complexity_level':i+1})

        save_instances_to_json(fewshots, FEWSHOT_DATA_PATH+'/{}_few_shots.json'.format(args.type))
        save_instances_to_json(all_generated, FEWSHOT_DATA_PATH+'/{}_all_generated.json'.format(args.type))

    return fewshots, all_generated

def save_instances_to_json(instances, file_path):
    with open(file_path, 'w') as f:
        json.dump(instances, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='EDP')
    parser.add_argument('--model', type=str, default='gpt-4')
    args = parser.parse_args()

    print('start ...')

    FEWSHOT_DATA_PATH = 'Data/{}/few_shot'.format(args.type)
    DATA_PATH = 'Data/{}'.format(args.type)
    MODEL= str(args.model)

    # Create a directory for data if it doesn't exist
    os.makedirs(FEWSHOT_DATA_PATH, exist_ok=True)
    generate_datapoint_function = generate_instances_function(args)
    run_gpt = run_gpt_function(args)
    complexity_params = generate_complexity_params(args)

    print('functions are all defined')

    # Load the test instances
    with open(DATA_PATH+'/{}_instances.json'.format(args.type.lower()), 'r') as f:
        test_data = json.load(f)

    instances, all_generated = generate_few_shot_instances(generate_datapoint_function, run_gpt, complexity_params, test_data,MODEL)

    # # Example usage:
    # num_instances = 10  # Number of instances to generate per complexity level
    # instances = generate_bsp_instances(num_instances, complexity_params)
    
    
    # save_instances_to_json(instances, FEWSHOT_DATA_PATH+'/{}_few_shots.json'.format(args.type))
    # save_instances_to_json(instances, FEWSHOT_DATA_PATH+'/{}_all_generated.json'.format(args.type))
