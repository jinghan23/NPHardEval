from models import run_gpt
from prompts import gcpPrompts, tspPrompts, mspPrompts
from old_scripts.check import gcpCheck, tspCheck, mspCheck
import os
import pandas as pd
import numpy as np
import json

def load_data(catgeory):
    if catgeory == 'gcp':
        data_path = '../Data/GCP/'
        all_data = []
        for file_num in range(10):
            with open(data_path+"synthesized_data_GCP_{}.txt".format(file_num)) as f:
                data = f.read()
            all_data += data.split('\n\n')
        return all_data
    elif catgeory == 'tsp':
        data_path = '../Data/TSP/'
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
    elif catgeory == 'msp':
        data_path = '../Data/MSP/'
        with open(data_path+"msp_instances.json", 'r') as f:
            all_data = json.load(f)
        return all_data
    else:
        print('Invalid category. Please choose from gcp, tsp, and msp.')
        return None

# run GCP
def runGCP(q, p=gcpPrompts): # q is the data for the HP-hard question, p is the prompt
    chromatic_number = q.split('\n')[0][-1] # last character of the first line
    number_of_vertices = q.split('\n')[1].split(' ')[2] # third word of the second line
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(max_vertices=number_of_vertices,max_colors=chromatic_number) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Option_no_reasoning'] + \
        '\n The graph is below: \n'
    for line in q.split('\n')[2:]:
        vertex_list = line.split(' ')
        this_line = "Vertex {} is connected to vertex {}.".format(vertex_list[1],vertex_list[2])
        prompt_text += this_line + '\n'
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

# run TSP
def runTSP(q, p=tspPrompts): # q is the data for the HP-hard question, p is the prompt
    total_cities = q.shape[0]
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(total_cities=total_cities) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Option_no_reasoning'] + \
        '\n The distances between cities are below: \n'
    for i in range(q.shape[0]):
        for j in range(q.shape[1]):
            if i < j: # only use the upper triangle
                this_line = "The path between City {} and City {} is with distance {}.".format(i,j,q.iloc[i,j])
                prompt_text += this_line + '\n'
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

# run MSP
def runMSP(q, p=mspPrompts): # q is the data for the HP-hard question, p is the prompt
    total_participants = q['participants']
    total_timeslots = q['time_slots']
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(total_participants=total_participants,total_timeslots=total_timeslots) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Option_no_reasoning'] + \
        '\n The meetings and participants details are as below: \n'
    meetings = q['meetings']
    participants = q['participants']
    for meeting in meetings:
        this_line = "Meeting {} is with duration {}.".format(meeting['id'],meeting['duration'])
        prompt_text += this_line + '\n'
    for j in participants.keys():
        this_line = "Participant {} is available at time slots {} and has meetings {}.".format(j,participants[j]['available_slots'],participants[j]['meetings'])
        prompt_text += this_line + '\n'
    print(prompt_text)
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

if __name__ == '__main__':
    RESULT_PATH = '../Results/'

    ### runGCP
    # load data
    gcpData = load_data('gcp')
    gcpResults = []
    for q in gcpData[:10]:
        output_dict = {}
        output = runGCP(q)
        output_dict['output'] = output
        correctness = gcpCheck(q,output)
        output_dict['correctness'] = correctness
        gcpResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+'gcpResults.json', 'a') as f:
        f.write(json.dumps(gcpResults) + '\n')
    
    # test runTSP
    tspData = load_data('tsp')
    tspResults = []
    for q in tspData[:10]:
        output_dict = {}
        output = runTSP(q)
        output_dict['output'] = output
        correctness = tspCheck(q,output)
        output_dict['correctness'] = correctness
        tspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+'tspResults.json', 'a') as f:
        f.write(json.dumps(tspResults) + '\n')

    
    # test runMSP
    mspData = load_data('msp')
    mspResults = []
    for q in mspData[:10]:
        output_dict = {}
        output = runMSP(q)
        output_dict['output'] = output
        correctness = mspCheck(q,output)
        output_dict['correctness'] = correctness
        mspResults.append(output_dict)
    # save the results
    with open(RESULT_PATH+'mspResults.json', 'a') as f:
        f.write(json.dumps(mspResults) + '\n')