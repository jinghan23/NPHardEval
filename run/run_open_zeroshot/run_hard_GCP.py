import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('../..')

from models import *
from prompts import gcpPrompts
from check.check_hard_GCP import *

import pandas as pd
import numpy as np
import json
from tqdm import tqdm

import argparse


def load_data():
    data_path = DATA_PATH
    all_data = []
    for file_num in range(10):
        with open(data_path+"synthesized_data_GCP_{}.txt".format(file_num)) as f:
            data = f.read()
        all_data += data.split('\n\n')[:-1]
    return all_data


def run_opensource_GCP(qs, p=gcpPrompts): # q is the data for the HP-hard question, p is the prompt
    all_prompts = []
    for q in tqdm(qs):
        chromatic_number = q.split('\n')[0][-1] # last character of the first line
        number_of_vertices = q.split('\n')[1].split(' ')[2] # third word of the second line
        prompt_text = p['Intro'] + '\n' \
            + p['Initial_question'].format(max_vertices=number_of_vertices,max_colors=chromatic_number) + '\n' \
            + p['Output_content'] + '\n' \
            + p['Output_format'] + \
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
    parser = argparse.ArgumentParser(description='Run model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Your script's logic here, using args.model as the model name
    MODEL = str(args.model)

    # MODEL = 'gpt-4-1106-preview'
    # # models: gpt-4-1106-preview, gpt-3.5-turbo-1106, claude-2, claude-instant, palm-2

    DATA_PATH = '../../Data/GCP/'
    RESULT_PATH = '../../Results/'


    # load data
    gcpData = load_data()
    print('number of datapoints: ', len(gcpData))
    gcpResults = []

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_GCP(gcpData)
    gcpResults = []
    for q, output in zip(gcpData, outputs):
        output_dict = {}
        output_dict['output'] = output
        correctness = gcpCheck(q,output)
        output_dict['correctness'] = correctness
        gcpResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'gcpResults.json', 'a') as f:
        f.write(json.dumps(gcpResults) + '\n')
