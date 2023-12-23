import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import bspPrompts
from check.check_p_BSP import *
import time

import pandas as pd
import numpy as np
import json
import argparse
from tqdm import tqdm

def load_data():
    data_path = DATA_PATH
    with open(data_path + "bsp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data


def run_opensource_BSP(args, qs, p=bspPrompts):
    all_prompts = []
    for i, q in enumerate(tqdm(qs)):
        target_value = q['target']
        # TO-DO: fix data not being sorted
        array = sorted(q['array'])
        prompt_text = p['Intro'] + '\n' + \
                  p['Initial_question'].format(target_value=target_value) + '\n' + \
                  p['Output_content'] + '\n' + \
                  p['Output_format'] + \
                  '\nAnswer:\n'
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
    parser = argparse.ArgumentParser(description='Run BSP model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../Data/BSP/'
    RESULT_PATH = '../Results/'

    # load data
    bspData = load_data()
    #bspData = bspData[:20]
    bspResults = []
    print('number of datapoints: ', len(bspData))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_BSP(args, bspData)
    for q, output in zip(bspData, outputs):
        output_dict = {}
        output_dict['output'] = output
        correctness = bsp_check(q,output)
        output_dict['correctness'] = correctness
        bspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'bspResults.json', 'w') as f:
        f.write(json.dumps(bspResults) + '\n')
