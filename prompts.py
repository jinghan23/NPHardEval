# TODO: add example (few shot) e.g., give fice examples with reasoning.
# can also add a few shot example for other problems.
# TODO: add connection to multi-round

# TODO:
# Add chain of thoughts
# Use XML tag for final answer <final_answer></final_answer>
# Add few shots: 4 examples for each question and their reasoning process

# P problems
sppPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

mfpPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

bspPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

# NP-complete problems
tspdPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

gcpdPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

kspPrompts = {
    "Intro": "",
    "Initial_question": "",
    "Output_content": "",
    "Output_format": "",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

# NP-hard problems
tspoPrompts = {
    "Intro": "The traveling salesman problem (TSP) is a classic optimization problem that aims to find the shortest possible route that visits a set of cities, with each city being visited exactly once and the route returning to the original city.",
    "Initial_question": "You must find the shortest path that visits all {total_cities} cities, labelled from 1 to {total_cities}. The distances between each pair of cities are provided.",
    "Output_content": "Please list each city in the order they are visited. Provide the total distance of the trip. You should also provide your step by step reasoning.",
    "Output_format": "Your output should contain two parts. First, your step by step reasoning wraped by <reasoning></reasoning>. Second, the final output of the result path and total distance wrapped by final_answer tag, like <final_answer>{'Path': '0->1->2->...->N->0', 'TotalDistance': INT_TOTAL_DISTANCE}</final_answer>",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

gcpoPrompts = {
    "Intro":"Graph coloring refers to the problem of coloring vertices of a graph in such a way that no two adjacent vertices have the same color. ",
    "Initial_question":"There are {max_vertices} vertices 1 to {max_vertices} in a graph. You may use {max_colors} colors with alphabats from A, B, C,... to color the graph.",
    "Output_content":"Please label every vertex, even if it is disconnected from the rest of the graph. Please provide each vertex's color. Do not skip any vertices. You should also provide your short step by step reasoning.",
    "Option_with_reasoning":" Your output should contain two parts. First, your step by step reasoning wraped by <reasoning></reasoning>. Second, the final output of all vertex numbers and their associated colors, wrapped by final_answer tag, like <final_answer>{0:'COLOR_1', 1:'COLOR_2', ...}</final_answer>.",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

mspoPrompts = {
    "Intro": "The meeting scheduling problem (MSP) is a type of constraint satisfaction problem where the goal is to find a suitable time slot for a meeting that all participants can attend without conflicts in their schedules.",
    "Initial_question": "There are {total_participants} participants with their available time slots. There are {total_timeslots} consecutive non-overlapping time slots. Let's assume all meetings has duration of 1.", 
    "Output_content": "Please provide a time slot where all participants can attend the meeting. You should also provide your step by step reasoning.",
    "Option_with_reasoning": "Your output should contain two parts. First, your step by step reasoning wraped by <reasoning></reasoning>. Second, the final output of meeting numbers followed by a list of slots, like <final_answer>{0:[1,2], 1:[4], ...}</final_answer>.",
    "Few_shot_self": "",
    "Few_shot_others": ""
}

# Deveplop later when coding for MAS
# feedbackPrompts = {
#     "Mentor":"Provide feedback for what and why the result is wrong. Can also provide high-level methodology guidence.", # simulated teacher feedback [a novel contribution]
#     "Learner":"Discuss about the wrong answer", # traditional self correction
#     "Wiki":"Share external knowledge without sharing the correct answer.", # tool
#     "Main_q_mentor":"",
#     "Main_q_learner":"",
#     "Main_q_wiki":"",
# }

# RQ: pattern - check which and where is the dominaent strategy discovered.
# RQ: pattern - check if more communication quantity lead to more correct answer or easier discovery of dominent strategy.
