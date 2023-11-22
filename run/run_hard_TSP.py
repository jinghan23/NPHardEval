import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import tspPrompts
from check.check_hard_TSP import *

import pandas as pd
import numpy as np
import json

DATA_PATH = '../Data/TSP/'
RESULT_PATH = '../Results/'
MODEL = 'gpt-4-1106-preview'
# others: gpt-3.5-turbo-1106, claude-2, claude-instant, palm-2

def load_data():
    data_path = DATA_PATH
    all_data = []
    for level in range(10):
        for file_num in range(10):
            #df = pd.read_csv(data_path+"synthesized_data_TSP_level_{}_instance_{}.csv".format(file_num,file_num+1))
            # read np arrary
            df = pd.read_csv(data_path+"synthesized_data_TSP_level_{}_instance_{}.csv".format(level,file_num+1),
                                header=None, 
                                index_col=False)
            # transform df to 
            all_data.append(df)
    return all_data

def runTSP(q, p=tspPrompts): # q is the data for the HP-hard question, p is the prompt
    total_cities = q.shape[0]
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(total_cities=total_cities) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Output_format'] + \
        '\n The distances between cities are below: \n'
    for i in range(q.shape[0]):
        for j in range(q.shape[1]):
            if i < j: # only use the upper triangle
                this_line = "The path between City {} and City {} is with distance {}.".format(i,j,q.iloc[i,j])
                prompt_text += this_line + '\n'
    output = run_gpt(prompt_text,model = MODEL)
    # remove \n in the output
    output = output.replace('\n','')
    return output

if __name__ == '__main__':
    tspData = load_data()
    tspResults = []
    for q in tspData[:10]:
        output_dict = {}
        output = runTSP(q)
        output_dict['output'] = output
        correctness = tspCheck(q,output)
        output_dict['correctness'] = correctness
        tspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'tspResults.json', 'a') as f:
        f.write(json.dumps(tspResults) + '\n')
