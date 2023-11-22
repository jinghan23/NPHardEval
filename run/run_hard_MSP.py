import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import *
from prompts import mspPrompts
from check.check_hard_MSP import *

import pandas as pd
import numpy as np
import json

DATA_PATH = '../Data/MSP/'
RESULT_PATH = '../Results/'
MODEL = 'gpt-4-1106-preview'
# others: gpt-3.5-turbo-1106, claude-2, claude-instant, palm-2

def load_data():
    data_path = DATA_PATH
    with open(data_path+"msp_instances.json", 'r') as f:
        all_data = json.load(f)
    return all_data

def runMSP(q, p=mspPrompts): # q is the data for the HP-hard question, p is the prompt
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
    # print(prompt_text)
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

if __name__ == '__main__':
    mspData = load_data()
    mspResults = []
    for q in mspData[:10]:
        output_dict = {}
        output = runMSP(q)
        output_dict['output'] = output
        correctness = mspCheck(q,output)
        output_dict['correctness'] = correctness
        mspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+MODEL+'_'+'mspResults.json', 'a') as f:
        f.write(json.dumps(mspResults) + '\n')