### Import Data
from data import Data

# print(Data)

### Import LLMs
# eg_prompt = 'how are you'
eg_prompt = 'Write the question set up in a elaborative way with latex math formula for 1) Graph coloring prpblem, 2) meeting scheduling problem, 3) Sudoku'

# GPT-3.5
from models import AzureGPT
azureGPT = AzureGPT()
print(azureGPT.get_gpt_output(eg_prompt))

# # Falcon
# from azure_falcon import AzureFalconDeployment
# # ad = AzureFalconDeployment('7b')
# ad40b = AzureFalconDeployment('40b')
# ad40b.get_output_azure_falcon(eg_prompt)

# # PaLM 2
# from google_palm import GooglePaLM
# palm = GooglePaLM()
# palm.get_palm_chat_output(eg_prompt)

# Claude 2 (TBD)

### Single LLM Reasoning Benchmark
# from prompt import reasoningPrompts, feedbackPrompts

# # GPT
# r = reasoningPrompts
# f = feedbackPrompts
# for q in Data[:3]:
#     chromatic_number = q.split('\n')[0][-1] # last character of the first line
#     number_of_vertices = q.split('\n')[1].split(' ')[2] # third word of the second line
#     prompt_text = r['Intro'] + '\n' \
#         + r['Initial_question'].format(max_vertices=number_of_vertices,max_colors=chromatic_number) + '\n' \
#         + r['Output_content'] + '\n' \
#         + r['Option_with_reasoning'] + \
#         '\n The graph is below: \n'
#     for line in q.split('\n')[2:]:
#         vertex_list = line.split(' ')
#         this_line = "Vertex {} is connected to vertex {}.".format(vertex_list[1],vertex_list[2])
#         prompt_text += this_line + '\n'
#     print(prompt_text)
#     print(azureGPT.get_gpt_output(prompt_text))
