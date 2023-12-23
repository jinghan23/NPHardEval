import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import tsp_dPrompts
from check.check_cmp_TSP_D import *
from tqdm import tqdm
import pandas as pd
import numpy as np
import json
import argparse
from utils import parse_xml_to_dict


def load_data():
    data_path = DATA_PATH
    all_data = []
    for level in range(10):
        for file_num in range(10):
            df = pd.read_csv(data_path + "decision_data_TSP_level_{}_instance_{}.csv".format(level, file_num + 1),
                             header=None, 
                             index_col=False)
            all_data.append(df)
    return all_data


def run_opensource_TSP_D(qs, p=tsp_dPrompts):
    all_prompts = []
    for q in tqdm(qs):
        threshold = q.iloc[-1, 0] # therashold is the last row
        adj_matrix = q.iloc[:-1].values # distance matrix is the rest of the rows
        total_cities = adj_matrix.shape[0] # exclude the last row
        prompt_text = p['Intro'] + '\n' + \
                    p['Initial_question'].format(total_cities=total_cities, distance_limit=threshold) + '\n' + \
                    p['Output_content'] + '\n' + \
                    p['Output_format'] + '\n' + \
                    'The distances between cities are below: \n'
        
        for i in range(adj_matrix.shape[0]):
            for j in range(adj_matrix.shape[1]):
                if i < j:  # only use the upper triangle
                    this_line = "The distance between City {} and City {} is {}.".format(i, j, adj_matrix[i, j])
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
    parser = argparse.ArgumentParser(description='Run TSP-D model script')

    # Add an argument for the model name
    parser.add_argument('model', type=str, help='The name of the model to run')

    # Parse the argument
    args = parser.parse_args()

    # Script logic using args.model as the model name
    MODEL = str(args.model)

    DATA_PATH = '../Data/TSP_Decision/'
    RESULT_PATH = '../Results/'

    tsp_d_Data = load_data()
    #tsp_d_Data = tsp_d_Data[:2]
    print(len(tsp_d_Data))
    tsp_d_Results = []

    outputs = run_opensource_TSP_D(tsp_d_Data)
    for result, instance in zip(outputs, tsp_d_Data):
        output_dict = {}
        threshold = instance.iloc[-1, 0] # therashold is the last row
        distance_matrix = instance.iloc[:-1].values # distance matrix is the rest of the rows
        output, reasoning = parse_xml_to_dict(result)
        output_dict['output'] = output
        output_dict['correctness'] = tsp_decision_check(distance_matrix, threshold, output)
        output_dict['reasoning'] = reasoning
        tsp_d_Results.append(output_dict)

    # Save the results
    with open(RESULT_PATH + MODEL + '_' + 'tsp_d_Results.json', 'a') as f:
        f.write(json.dumps(tsp_d_Results) + '\n')
