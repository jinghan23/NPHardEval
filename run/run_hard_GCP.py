import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import gcpPrompts
from check.check_hard_GCP import *

import pandas as pd
import numpy as np
import json

DATA_PATH = '../Data/GCP/'
RESULT_PATH = '../Results/'
MODEL = 'gpt-4-1106-preview'
# others: gpt-3.5-turbo-1106, claude-2, claude-instant, palm-2

def load_data():
    data_path = DATA_PATH
    all_data = []
    for file_num in range(10):
        with open(data_path+"synthesized_data_GCP_{}.txt".format(file_num)) as f:
            data = f.read()
        all_data += data.split('\n\n')
    return all_data

def runGCP(q, p=gcpPrompts): # q is the data for the HP-hard question, p is the prompt
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
    output = run_gpt(prompt_text,model = MODEL)
    return output

if __name__ == '__main__':
    # load data
    gcpData = load_data()
    gcpResults = []
    for q in gcpData[:10]:
        output_dict = {}
        output = runGCP(q)
        output_dict['output'] = output
        correctness = gcpCheck(q,output)
        output_dict['correctness'] = correctness
        gcpResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'gcpResults.json', 'a') as f:
        f.write(json.dumps(gcpResults) + '\n')
