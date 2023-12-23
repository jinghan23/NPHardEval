import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import edpPrompts
from check.check_p_EDP import *
from tqdm import tqdm
import time

import json
import argparse

def load_data():
    data_path = DATA_PATH
    with open(data_path + "edp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data

def run_opensource_EDP(args, qs, p=edpPrompts):
    all_prompts = []
    for i, q in enumerate(tqdm(qs)):
        string_a = q['string_a']
        string_b = q['string_b']
        prompt_text = p['Intro'] + '\n' + \
                    p['Initial_question'].format(string_a=string_a, string_b=string_b) + '\n' + \
                    p['Output_content'] + '\n' + \
                    p['Output_format']
        prompt_text += 'Answer:\n'
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
    parser = argparse.ArgumentParser(description='Run EDP model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Create the parser
    parser = argparse.ArgumentParser(description='Run EDP model script')

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../Data/EDP/'
    RESULT_PATH = '../Results/'

    # load data
    edpData = load_data()
    #edpData = edpData[:2]
    edpResults = []
    print('number of datapoints: ', len(edpData))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_EDP(args, edpData)
    for q, output in zip(edpData, outputs):
        output_dict = {}
        parsed_result, reasoning = parse_xml_to_dict(output)
        output_dict['output'] = parsed_result
        correctness = edp_check(q,parsed_result)
        output_dict['correctness'] = correctness
        edpResults.append(output_dict)
    with open(RESULT_PATH+MODEL+'_'+'edpResults.json', 'w') as f:
        f.write(json.dumps(edpResults) + '\n')
