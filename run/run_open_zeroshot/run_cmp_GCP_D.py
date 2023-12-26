import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('../..')

from models import *
from prompts import gcp_dPrompts
from check.check_cmp_GCP_D import *

import pandas as pd
import numpy as np
import json
import argparse
from tqdm import tqdm 

def load_data():
    data_path = DATA_PATH
    all_data = []
    for file_num in range(10):
        with open(data_path + "decision_data_GCP_{}.txt".format(file_num)) as f:
            data = f.read()
        all_data += data.split('\n\n')[:-1]
    return all_data


def run_opensource_GCP_D(qs, p=gcp_dPrompts):
    all_prompts = []
    for q in tqdm(qs):
        number_of_colors = q.split('\n')[0].split()[-2] # last character of the first line
        number_of_vertices = q.split('\n')[1].split(' ')[2] # third word of the second line
        prompt_text = p['Intro'] + '\n' + \
                    p['Initial_question'].format(total_vertices=number_of_vertices, number_of_colors=number_of_colors) + '\n' + \
                    p['Output_content'] + '\n' + \
                    p['Output_format'] + '\n' + \
                        '\n The graph is below: \n'
        for line in q.split('\n')[2:]:
            vertex_list = line.split(' ')
            this_line = "Vertex {} is connected to vertex {}.".format(vertex_list[1],vertex_list[2])
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
    parser = argparse.ArgumentParser(description='Run GCP-D model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../../Data/Zeroshot/GCP_Decision/'
    RESULT_PATH = '../../Results/'

    # load data
    gcp_d_Data = load_data()
    #gcp_d_Data = gcp_d_Data[:20]
    gcpdResults = []
    print('number of datapoints: ', len(gcp_d_Data))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_GCP_D(gcp_d_Data)
    for q, output in zip(gcp_d_Data, outputs):
        output_dict = {}
        number_of_colors = int(q.split('\n')[0].split()[-2])
        output, reasoning = parse_xml_to_dict(output)
        output_dict['output'] = output
        output_dict['correctness'] = gcp_decision_check(q, output, number_of_colors)
        output_dict['reasoning'] = reasoning
        gcpdResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'gcp_d_Results.json', 'a') as f:
        f.write(json.dumps(gcpdResults) + '\n')
