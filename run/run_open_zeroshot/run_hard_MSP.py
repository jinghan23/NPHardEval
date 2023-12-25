import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('../..')

from models import *
from prompts import mspPrompts
from check.check_hard_MSP import *

import pandas as pd
import numpy as np
import json
from tqdm import tqdm

import argparse

def load_data():
    data_path = DATA_PATH
    with open(data_path+"msp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data


def run_opensource_MSP(qs, p=mspPrompts): # q is the data for the HP-hard question, p is the prompt
    all_prompts = []
    for q in tqdm(qs):
        total_participants = q['participants']
        total_timeslots = q['time_slots']
        prompt_text = p['Intro'] + '\n' \
            + p['Initial_question'].format(total_participants=total_participants,total_timeslots=total_timeslots) + '\n' \
            + p['Output_content'] + '\n' \
            + p['Output_format'] + \
            '\n The meetings and participants details are as below: \n'
        meetings = q['meetings']
        participants = q['participants']
        for meeting in meetings:
            this_line = "Meeting {} is with duration {}.".format(meeting['id'],meeting['duration'])
            prompt_text += this_line + '\n'
        for j in participants.keys():
            this_line = "Participant {} is available at time slots {} and has meetings {}.".format(j,participants[j]['available_slots'],participants[j]['meetings'])
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

    DATA_PATH = '../../Data/Zeroshot/MSP/'
    RESULT_PATH = '../../Results/'


    # load data
    mspData = load_data()
    print('number of datapoints: ', len(mspData))

    print("Using model: {}".format(MODEL))

    outputs = run_opensource_MSP(mspData)
    mspResults = []
    for q, output in zip(mspData, outputs):
        output_dict = {}
        output_dict['output'] = output
        correctness = mspCheck(q,output)
        output_dict['correctness'] = correctness
        mspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'mspResults.json', 'a') as f:
        f.write(json.dumps(mspResults) + '\n')
