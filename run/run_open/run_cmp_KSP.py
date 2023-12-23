import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import kspPrompts
from check.check_cmp_KSP import *

import pandas as pd
import numpy as np
import json
import argparse
from tqdm import tqdm

def load_data():
    data_path = DATA_PATH
    with open(data_path + "ksp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data

def run_opensource_KSP(qs, p=kspPrompts):
    all_prompts = []
    for q in tqdm(qs):
        knapsack_capacity = q['knapsack_capacity']
        items = q['items']
        prompt_text = p['Intro'] + '\n' + \
                    p['Initial_question'].format(knapsack_capacity=knapsack_capacity) + '\n' + \
                    p['Output_content'] + '\n' + \
                    p['Output_format'] + \
                    '\n The items details are as below: \n'
        for item in items:
            this_line = f"Item {item['id']} has weight {item['weight']} and value {item['value']}."
            prompt_text += this_line + '\n'
        all_prompts.append(prompt_text)

    if MODEL.startswith('mistral'):
        output = run_mistral(all_prompts)
    elif MODEL.startswith('yi'):
        output = run_yi(all_prompts)
    elif MODEL.startswith('mpt'):
        output = run_mpt(all_prompts)
    elif MODEL.startswith('phi'):
        output = run_phi(all_prompts)
    elif MODEL.startswith('vicuna'):
        output = run_vicuna(all_prompts)
    else:
        raise NotImplementedError
    return output


if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Run KSP model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../Data/KSP/'
    RESULT_PATH = '../Results/'

    # load data
    kspData = load_data()
    #kspData = kspData[:20]
    kspdResults = []
    print('number of datapoints: ', len(kspData))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_KSP(kspData)
    for q, output in zip(kspData, outputs):
        output_dict = {}
        output, reasoning = parse_xml_to_dict(output)
        output_dict['output'] = output
        output_dict['correctness'] = kspCheck(q, output)
        output_dict['reasoning'] = reasoning
        kspdResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'kspResults.json', 'a') as f:
        f.write(json.dumps(kspdResults) + '\n')
