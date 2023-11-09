tspPrompts = {
    "Intro": "The traveling salesman problem (TSP) is a classic optimization problem that aims to find the shortest possible route that visits a set of cities, with each city being visited exactly once and the route returning to the original city.",
    "Initial_question": "You must find the shortest path that visits all {total_cities} cities, labelled from 1 to {total_cities}. The distances between each pair of cities are provided.",
    "Output_content": "Please list each city in the order they are visited. Provide the total distance of the trip. The output should include each city's number, and the total distance should be on a new line at the end, formatted as 'Total Distance: {TOTAL DISTANCE}'.",
    "Option_no_reasoning": "You should not provide any reasoning or explanation in your answer. Your output should be in the format of a list of cities in the order they are visited, for example, '{'Answer': '0->1->2->...->N->0', 'TotalDistance': a number}'.",
    "Option_with_reasoning": "You should also provide your step by step reasoning. Your output should be in the format '{'Answer': '0->1->2->...->N->0'}', 'TotalDistance': a number, 'Reasoning': a step by step walkthrough}'.",
    "Wrong_answer": "This is incorrect. Using the feedback, please try again."
}

mspPrompts = {
    "Intro": "The meeting scheduling problem (MSP) is a type of constraint satisfaction problem where the goal is to find a suitable time slot for a meeting that all participants can attend without conflicts in their schedules.",
    "Initial_question": "There are {total_participants} participants with their available time slots. There are {total_timeslots} consecutive non-overlapping time slots. Meetings may also have different durations from 1 to 3 slots.",
    "Output_content": "Please provide a time slot where all participants can attend the meeting. The output should be formatted as meeting number followed by a list of slots.",
    "Option_no_reasoning": "Do not include any reasoning or explanation in your answer. Your output should be in the format '{'Answer': '{'0:[1,2], 1:[4], ...'}'}'.",
    "Option_with_reasoning": "You should also include your step by step reasoning for selecting the time slot. Your output should be in the format '{'Answer': '{'0:[1,2], 1:[4], ...'}', 'Reasoning': a step by step walkthrough}'.",
    "Wrong_answer": "This is incorrect. Please review the available times and try to find a suitable slot again."
}

gcpPrompts = {
    "Intro":"Graph coloring refers to the problem of coloring vertices of a graph in such a way that no two adjacent vertices have the same color. ",
    "Initial_question":"There are {max_vertices} vertices 1 to {max_vertices} in a graph. You may use {max_colors} colors with alphabats from A, B, C,... to color the graph.",
    "Output_content":"Please label every vertex, even if it is disconnected from the rest of the graph. Please provide each vertex's color. Do not skip any vertices. Each color must be provided on a new line in the response and should be formatted as '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}'.",
    "Option_no_reasoning":"You should not provide anything beyond the answer. You output should be in the format '{'Answer': a list of '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}'.",
    "Option_with_reasoning":"You should also provide your short step by step reasoning. You output should be in the format '{'Answer': a list of '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}','Reasoning: a step by step walk through'}'.",
    "Wrong_answer":"This is incorrect. Using the feedback, please try again."
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
