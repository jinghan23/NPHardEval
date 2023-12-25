import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('../..')

from models import *
from prompts import sppPrompts
from check.check_p_SPP import *
from tqdm import tqdm
import pandas as pd
import numpy as np
import json
import argparse

def load_data():
    data_path = DATA_PATH
    with open(data_path + "spp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data


def run_opensource_SPP(qs, p=sppPrompts):
    all_prompts = []
    for q in tqdm(qs):
        start_node = q['nodes'][0]
        end_node = q['nodes'][-1]
        edges = q['edges']
        prompt_text = p['Intro'] + '\n' + \
                    p['Initial_question'].format(start_node=start_node, end_node=end_node) + '\n' + \
                    p['Output_content'] + '\n' + \
                    p['Output_format'] + \
                    "\n The graph's edges and weights are as follows: \n"
        for edge in edges:
            this_line = f"Edge from {edge['from']} to {edge['to']} has a weight of {edge['weight']}."
            prompt_text += this_line + '\n'
        prompt_text += 'Answer:[/INST]\n'
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
    parser = argparse.ArgumentParser(description='Run SPP model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../../Data/SPP/'
    RESULT_PATH = '../../Results/'


    # load data
    sppData = load_data()
    #sppData = sppData[:10]
    sppResults = []
    print('number of datapoints: ', len(sppData))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_SPP(sppData)
    for q, output in zip(sppData, outputs):
        output_dict = {}
        output, reasoning = parse_xml_to_dict(output)
        output_dict['output'] = output
        output_dict['correctness'] = spp_check(q, output)
        output_dict['reasoning'] = reasoning
        sppResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'sppResults.json', 'w') as f:
        f.write(json.dumps(sppResults) + '\n')
