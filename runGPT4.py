from models import run_gpt
from prompts import gcpPrompts, tspPrompts, mspPrompts
from check import gcpCheck, tspCheck, mspCheck
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
                df = pd.read_csv(data_path+"synthesized_data_TSP_level_{}_instance_{}.csv".format(level,file_num+1))
                data = df.to_numpy()
                # transform df to 
                all_data.append(data)
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

# run TSP - to convert
def runTSP(q, p=tspPrompts): # q is the data for the HP-hard question, p is the prompt
    number_of_vertices = q.shape[0]
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(max_vertices=number_of_vertices) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Option_no_reasoning'] + \
        '\n The graph is below: \n'
    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            if q[i,j] > 0:
                this_line = "Vertex {} is connected to vertex {} with distance {}.".format(i,j,q[i,j])
                prompt_text += this_line + '\n'
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

# run MSP - to convert
def runMSP(q, p=mspPrompts): # q is the data for the HP-hard question, p is the prompt
    number_of_vertices = q.shape[0]
    prompt_text = p['Intro'] + '\n' \
        + p['Initial_question'].format(max_vertices=number_of_vertices) + '\n' \
        + p['Output_content'] + '\n' \
        + p['Option_no_reasoning'] + \
        '\n The graph is below: \n'
    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            if q[i,j] > 0:
                this_line = "Vertex {} is connected to vertex {} with distance {}.".format(i,j,q[i,j])
                prompt_text += this_line + '\n'
    output = run_gpt(prompt_text,model = "gpt-4")
    return output

if __name__ == '__main__':
    # test runGCP
    gcpData = load_data('gcp')
    for q in gcpData[:10]:
        output = runGCP(q)
        print(output)
        print(gcpCheck(q,output))
    
    # # test runTSP
    # tspData = load_data('tsp')
    # for q in tspData[:1]:
    #     print(q)
    #     # output = runTSP(q)
    #     # print(output)
    #     # print(tspCheck(q,output))
    
    # # test runMSP
    # mspData = load_data('msp')
    # for q in mspData[:1]:
    #     print(q)
    #     # output = runMSP(q)
    #     # print(output)
    #     # print(mspCheck(q,output))